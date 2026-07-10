import { create } from 'zustand';

export interface PendingUploadFile {
  file: File;
  detectedCategory: 'assets' | 'books' | 'notes' | 'media' | 'archives' | 'projects';
  destination: 'A' | 'B';
  customCategory?: string;
  progress?: number;
  status: 'pending' | 'uploading' | 'success' | 'error';
  error?: string;
}

interface UploadCenterState {
  isOpen: boolean;
  files: PendingUploadFile[];
  setOpen: (open: boolean) => void;
  addFiles: (newFiles: File[]) => void;
  removeFile: (index: number) => void;
  updateFileCategory: (index: number, category: PendingUploadFile['detectedCategory']) => void;
  updateFileDestination: (index: number, destination: PendingUploadFile['destination']) => void;
  startUploads: (token: string | null) => Promise<void>;
  clear: () => void;
}

export const useUploadCenter = create<UploadCenterState>((set, get) => ({
  isOpen: false,
  files: [],
  setOpen: (open) => set({ isOpen: open }),
  addFiles: (newFiles) => {
    const pending = newFiles.map((file) => {
      // Auto classify
      const ext = file.name.split('.').pop()?.toLowerCase();
      let cat: PendingUploadFile['detectedCategory'] = 'assets';
      if (ext === 'pdf') cat = 'books';
      else if (ext === 'md' || ext === 'txt') cat = 'notes';
      else if (['mp4', 'mov', 'avi', 'mkv', 'webm', 'mp3', 'wav'].includes(ext || '')) cat = 'media';
      else if (['zip', 'tar', 'gz', 'sql', 'rar'].includes(ext || '')) cat = 'archives';
      else if (['json', 'js', 'ts', 'tsx', 'py', 'go'].includes(ext || '')) cat = 'projects';

      return {
        file,
        detectedCategory: cat,
        destination: (cat === 'assets' || cat === 'media' ? 'B' : 'A') as 'A' | 'B',
        status: 'pending' as const,
      };
    });
    set((state) => ({ files: [...state.files, ...pending], isOpen: true }));
  },
  removeFile: (index) =>
    set((state) => ({ files: state.files.filter((_, i) => i !== index) })),
  updateFileCategory: (index, category) =>
    set((state) => {
      const copy = [...state.files];
      copy[index] = { ...copy[index], detectedCategory: category };
      return { files: copy };
    }),
  updateFileDestination: (index, destination) =>
    set((state) => {
      const copy = [...state.files];
      copy[index] = { ...copy[index], destination };
      return { files: copy };
    }),
  startUploads: async (token) => {
    const state = get();
    const filesToUpload = state.files.filter((f) => f.status === 'pending');
    if (filesToUpload.length === 0) return;

    for (let i = 0; i < state.files.length; i++) {
      const f = state.files[i];
      if (f.status !== 'pending') continue;

      set((state) => {
        const copy = [...state.files];
        copy[i] = { ...copy[i], status: 'uploading', progress: 10 };
        return { files: copy };
      });

      const formData = new FormData();
      formData.append('file', f.file);
      formData.append('category', f.detectedCategory);

      try {
        const headers: Record<string, string> = {};
        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`/api/storage/upload?target_label=${f.destination}`, {
          method: 'POST',
          headers,
          body: formData,
          credentials: 'include',
        });

        if (!response.ok) throw new Error('Upload failed');

        set((state) => {
          const copy = [...state.files];
          copy[i] = { ...copy[i], status: 'success', progress: 100 };
          return { files: copy };
        });
      } catch (err: any) {
        set((state) => {
          const copy = [...state.files];
          copy[i] = {
            ...copy[i],
            status: 'error',
            progress: 0,
            error: err.message || 'Error occurred',
          };
          return { files: copy };
        });
      }
    }
  },
  clear: () => set({ files: [], isOpen: false }),
}));
