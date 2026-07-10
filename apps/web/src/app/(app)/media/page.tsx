'use client';

import { useState, useEffect } from 'react';
import { Film, PlayCircle, Search, Trash2, Download, Loader2, RefreshCw } from 'lucide-react';
import { api, getAccessToken } from '@/lib/api';

interface MediaFile {
  id: string;
  name: string;
  mimeType: string;
  size?: string;
  modifiedTime: string;
  provider_id?: string;
}

export default function MediaCenterPage() {
  const [mediaList, setMediaList] = useState<MediaFile[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  const loadMedia = async () => {
    setLoading(true);
    try {
      const res = await api<{ files: MediaFile[] }>('/api/storage/list?folder_id=root');
      const filtered = (res.files || []).filter(
        (f) =>
          f.mimeType.startsWith('video/') ||
          f.mimeType.startsWith('audio/') ||
          f.name.toLowerCase().endsWith('.mp4') ||
          f.name.toLowerCase().endsWith('.mov') ||
          f.name.toLowerCase().endsWith('.mp3')
      );
      setMediaList(filtered);
    } catch (err) {
      console.error('Failed to load media items:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMedia();
  }, []);

  const handleDownload = async (file: MediaFile) => {
    try {
      const providerQuery = file.provider_id ? `?provider_id=${file.provider_id}` : '';
      const response = await fetch(`/api/storage/download/${file.id}${providerQuery}`, {
        headers: {
          Authorization: `Bearer ${getAccessToken()}`,
        },
        credentials: 'include',
      });
      if (!response.ok) throw new Error('Download failed');
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = file.name;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert('Failed to download media item.');
      console.error(err);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in text-foreground h-[calc(100vh-80px)] overflow-hidden flex flex-col">
      {/* System Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">Media Hub</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <Film className="h-7 w-7 text-primary" />
            Media Center
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Streaming center for uploaded videos, recordings, soundtracks, and media archives.
          </p>
        </div>

        {/* Search */}
        <div className="flex items-center gap-3">
          <div className="relative w-full sm:w-60">
            <input
              type="text"
              placeholder="Search media..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-md border border-border bg-background py-1.5 pl-8 pr-3 text-xs outline-none focus:border-primary text-foreground"
            />
            <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-muted-foreground" />
          </div>
          <button
            onClick={loadMedia}
            className="p-2 hover:bg-accent rounded-lg border border-border transition-colors text-muted-foreground hover:text-foreground"
            title="Refresh list"
          >
            <RefreshCw className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

      {/* Media Items List */}
      <div className="flex-1 overflow-y-auto pb-12 pr-2">
        {loading ? (
          <div className="flex h-[40vh] items-center justify-center">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        ) : mediaList.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-center text-muted-foreground">
            <Film className="h-12 w-12 mb-3 text-muted-foreground/35" />
            <p className="text-sm font-semibold">No media items found</p>
            <p className="text-xs mt-1">Upload mp4/mov video files to auto-route them here.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {mediaList
              .filter((m) => m.name.toLowerCase().includes(searchQuery.toLowerCase()))
              .map((file) => (
                <div
                  key={file.id}
                  className="rounded-xl border border-border bg-card/45 p-4 flex flex-col justify-between hover:border-primary/20 transition-all hover:-translate-y-0.5 shadow-sm"
                >
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                      <PlayCircle className="h-5 w-5" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="text-xs font-semibold truncate text-foreground leading-tight">{file.name}</p>
                      <p className="text-3xs text-muted-foreground mt-0.5 font-mono">
                        {new Date(file.modifiedTime).toLocaleDateString()}
                      </p>
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-border/40 flex justify-end gap-2">
                    <button
                      onClick={() => handleDownload(file)}
                      className="rounded border border-border hover:border-primary px-3 py-1 text-3xs font-semibold text-foreground hover:bg-primary/5 transition-all flex items-center gap-1"
                    >
                      <Download className="h-3 w-3" /> Download
                    </button>
                  </div>
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );
}
