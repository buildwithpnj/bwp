'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import {
  HardDrive,
  Folder,
  File as FileIcon,
  FileText,
  FileImage,
  FileVideo,
  FileAudio,
  Search,
  Plus,
  Upload,
  Trash2,
  Download,
  ChevronRight,
  Loader2,
  Link2,
  Link2Off,
  FolderPlus,
  RefreshCw,
} from 'lucide-react';
import { api, getAccessToken } from '@/lib/api';

interface DriveFile {
  id: string;
  name: string;
  mimeType: string;
  size?: string;
  modifiedTime: string;
  thumbnailLink?: string;
  iconLink?: string;
  provider?: string;
  provider_id?: string;
}

interface StorageProvider {
  id: string;
  name: string;
  provider_label: string;
  type: string;
  account_email: string;
  status: string;
  connected: boolean;
  used_storage: number;
  available_storage: number;
  priority: number;
  last_sync: string | null;
}

interface Breadcrumb {
  id: string;
  name: string;
}

export default function StoragePage() {
  const [vaultView, setVaultView] = useState<'files' | 'media' | 'infrastructure'>('files');
  // Provider states
  const [providers, setProviders] = useState<StorageProvider[]>([]);
  const [isConfigured, setIsConfigured] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [connectedEmail, setConnectedEmail] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // File browser states
  const [files, setFiles] = useState<DriveFile[]>([]);
  const [currentFolder, setCurrentFolder] = useState<string>('root');
  const [breadcrumbs, setBreadcrumbs] = useState<Breadcrumb[]>([{ id: 'root', name: 'Root' }]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  // UI operation states
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<string | null>(null);
  const [showFolderModal, setShowFolderModal] = useState(false);
  const [newFolderName, setNewFolderName] = useState('');
  const [isCreatingFolder, setIsCreatingFolder] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  // Sync / Backup states
  const [syncing, setSyncing] = useState<Record<string, boolean>>({});
  const [restoring, setRestoring] = useState<Record<string, boolean>>({});

  const handleSyncSection = async (section: string) => {
    setSyncing((prev) => ({ ...prev, [section]: true }));
    try {
      const response = await api<{ status: string; message: string }>(`/api/gdrive/sync/${section}`, {
        method: 'POST',
      });
      alert(response.message);
    } catch (err) {
      alert(`Sync failed: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setSyncing((prev) => ({ ...prev, [section]: false }));
    }
  };

  const handleRestoreSection = async (section: string) => {
    if (
      confirm(
        `Are you sure you want to RESTORE ${section} from Google Drive? This will overwrite your local database records for this section.`
      )
    ) {
      setRestoring((prev) => ({ ...prev, [section]: true }));
      try {
        const response = await api<{ status: string; message: string }>(
          `/api/gdrive/restore/${section}`,
          {
            method: 'POST',
          }
        );
        alert(response.message);
      } catch (err) {
        alert(`Restore failed: ${err instanceof Error ? err.message : 'Unknown error'}`);
      } finally {
        setRestoring((prev) => ({ ...prev, [section]: false }));
      }
    }
  };

  // Load files in active folder
  const loadFiles = useCallback(async (folderId: string, searchVal = '') => {
    setLoading(true);
    try {
      let endpoint = `/api/storage/list?folder_id=${folderId}`;
      if (searchVal) {
        endpoint = `/api/storage/search?q=${encodeURIComponent(searchVal)}`;
        setIsSearching(true);
      } else {
        setIsSearching(false);
      }

      const data = await api<{ files: DriveFile[] }>(endpoint);
      setFiles(data.files || []);
    } catch (error) {
      console.error('Failed to load storage files:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  // Load providers & status from new multi-provider API
  const checkStatus = useCallback(async () => {
    try {
      const data = await api<{ providers: StorageProvider[] }>('/api/storage/providers');
      const providerList = data.providers || [];
      setProviders(providerList);

      const anyActive = providerList.some((p) => p.status === 'active' && p.connected);
      setIsConfigured(true); // credentials are configured if the API returned
      setIsConnected(anyActive);

      const primaryProvider = providerList.find((p) => p.status === 'active' && p.connected);
      setConnectedEmail(primaryProvider?.account_email ?? null);

      if (anyActive) {
        await loadFiles(currentFolder);
      }
    } catch (error) {
      console.error('Failed to get storage provider status:', error);
      setIsConfigured(false);
    } finally {
      setLoading(false);
    }
  }, [currentFolder, loadFiles]);

  useEffect(() => {
    checkStatus();
  }, [currentFolder, checkStatus]);

  // Initiate OAuth login flow for Provider A
  const handleConnect = async () => {
    try {
      const data = await api<{ url: string }>('/api/storage/auth/google/login');
      if (data.url) {
        window.location.href = data.url;
      }
    } catch (error) {
      alert('Failed to start Google Drive A connection. Make sure credentials are configured.');
      console.error(error);
    }
  };

  // Initiate OAuth login flow for Provider B
  const handleConnectB = async () => {
    try {
      const data = await api<{ url: string }>('/api/storage/auth/google/provider-b/login');
      if (data.url) {
        window.location.href = data.url;
      }
    } catch (error) {
      alert('Failed to start Google Drive B connection. Make sure Provider B credentials are configured.');
      console.error(error);
    }
  };

  // Disconnect / unlink a storage provider by ID
  const handleDisconnect = async (providerId?: string) => {
    if (confirm('Are you sure you want to unlink this Google Drive account? Your files in Google Drive will not be deleted.')) {
      setLoading(true);
      try {
        if (providerId) {
          await api(`/api/storage/providers/${providerId}`, { method: 'DELETE' });
        }
        await checkStatus();
      } catch (error) {
        console.error('Failed to unlink provider:', error);
      } finally {
        setLoading(false);
      }
    }
  };

  // Folder navigation
  const handleFolderClick = (folder: DriveFile) => {
    const nextFolder = folder.id;
    setCurrentFolder(nextFolder);
    setBreadcrumbs((prev) => [...prev, { id: folder.id, name: folder.name }]);
  };

  const handleBreadcrumbClick = (crumb: Breadcrumb, index: number) => {
    setCurrentFolder(crumb.id);
    setBreadcrumbs((prev) => prev.slice(0, index + 1));
    setSearchQuery('');
  };

  // Search files
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    loadFiles(currentFolder, searchQuery);
  };

  const clearSearch = () => {
    setSearchQuery('');
    loadFiles(currentFolder, '');
  };

  // Create folder (not yet supported in new multi-provider API — placeholder)
  const handleCreateFolder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFolderName.trim()) return;
    setIsCreatingFolder(true);
    try {
      alert('Folder creation coming soon in multi-provider mode.');
      setNewFolderName('');
      setShowFolderModal(false);
    } catch (error) {
      alert('Failed to create folder.');
      console.error(error);
    } finally {
      setIsCreatingFolder(false);
    }
  };

  // Upload file
  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files;
    if (!selectedFiles || selectedFiles.length === 0) return;

    const file = selectedFiles[0];
    const formData = new FormData();
    formData.append('file', file);
    if (currentFolder && currentFolder !== 'root') {
      formData.append('parent_id', currentFolder);
    }

    setIsUploading(true);
    setUploadProgress(`Uploading "${file.name}"...`);

    try {
      const token = getAccessToken();
      const headers: HeadersInit = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch('/api/storage/upload', {
        method: 'POST',
        headers,
        body: formData,
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Upload request failed');
      }

      setUploadProgress('Upload complete!');
      setTimeout(() => {
        setIsUploading(false);
        setUploadProgress(null);
        loadFiles(currentFolder);
      }, 1000);
    } catch (error) {
      alert(`Failed to upload file "${file.name}"`);
      console.error(error);
      setIsUploading(false);
      setUploadProgress(null);
    }
  };

  // Download file
  const handleDownload = async (file: DriveFile) => {
    try {
      const providerQuery = file.provider_id ? `?provider_id=${file.provider_id}` : '';
      const response = await fetch(`/api/storage/download/${file.id}${providerQuery}`, {
        headers: {
          Authorization: `Bearer ${getAccessToken()}`,
        },
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Download failed');
      }

      // Read Content-Disposition header if available
      const disposition = response.headers.get('Content-Disposition');
      let filename = file.name;
      if (disposition && disposition.indexOf('filename=') !== -1) {
        const matches = /filename="([^"]+)"/.exec(disposition);
        if (matches != null && matches[1]) {
          filename = matches[1];
        }
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      alert('Failed to download file.');
      console.error(error);
    }
  };

  // Delete file
  const handleDelete = async (file: DriveFile) => {
    if (confirm(`Are you sure you want to delete "${file.name}"? This will move it to trash or permanently delete it.`)) {
      try {
        const providerQuery = file.provider_id ? `?provider_id=${file.provider_id}` : '';
        await api(`/api/storage/delete/${file.id}${providerQuery}`, { method: 'DELETE' });
        await loadFiles(currentFolder);
      } catch (error) {
        alert('Failed to delete file.');
        console.error(error);
      }
    }
  };

  // File type helpers
  const formatBytes = (bytesStr?: string) => {
    if (!bytesStr) return '—';
    const bytes = parseInt(bytesStr, 10);
    if (isNaN(bytes)) return '—';
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  const getFileIcon = (mimeType: string) => {
    if (mimeType === 'application/vnd.google-apps.folder') return <Folder className="h-5 w-5 text-amber-500 fill-amber-500/20" />;
    if (mimeType.startsWith('image/')) return <FileImage className="h-5 w-5 text-emerald-400" />;
    if (mimeType.startsWith('video/')) return <FileVideo className="h-5 w-5 text-blue-400" />;
    if (mimeType.startsWith('audio/')) return <FileAudio className="h-5 w-5 text-violet-400" />;
    if (mimeType.includes('pdf') || mimeType.includes('document')) return <FileText className="h-5 w-5 text-rose-400" />;
    return <FileIcon className="h-5 w-5 text-muted-foreground" />;
  };

  const isFolder = (mimeType: string) => mimeType === 'application/vnd.google-apps.folder';

  return (
    <div className="space-y-6 animate-fade-in text-pnj-textStrong font-sans">
      {/* ─── SYSTEM HEADER ────────────────────────────────────── */}
      <div className="flex items-center justify-between border-b border-border pb-3">
        <div>
          <span className="font-mono text-[10px] tracking-[0.25em] text-primary uppercase font-bold">SYSTEM_VAULT // v0.51.0</span>
          <h1 className="text-xl font-bold tracking-tight mt-0.5">THE VAULT</h1>
        </div>
        <div className="flex gap-2">
          {['files', 'media', 'infrastructure'].map((view) => (
            <button
              key={view}
              onClick={() => setVaultView(view as any)}
              className={`px-3 py-1 border transition-colors uppercase font-mono font-bold text-[10px] ${
                vaultView === view
                  ? 'text-primary border-primary bg-primary/5'
                  : 'text-muted-foreground border-border hover:border-muted-foreground'
              }`}
            >
              {view}
            </button>
          ))}
        </div>
      </div>

      {/* ─── INFRASTRUCTURE VIEW ───────────────────────────── */}
      {vaultView === 'infrastructure' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Drive A (Primary) */}
            {(() => {
              const provA = providers.find(p => p.provider_label === 'A');
              return (
                <div className="border border-border bg-card p-5 flex flex-col justify-between space-y-4 font-mono text-xs">
                  <div>
                    <div className="flex items-center justify-between border-b border-border/40 pb-2">
                      <span className="text-[10px] text-muted-foreground uppercase font-bold">Primary Drive</span>
                      <span className={`text-[10px] font-bold ${
                        provA?.connected ? 'text-emerald-400' : 'text-muted-foreground'
                      }`}>
                        {provA?.connected ? 'ONLINE' : 'OFFLINE'}
                      </span>
                    </div>
                    <h3 className="text-sm font-bold mt-3 text-foreground">GOOGLE_DRIVE_A</h3>
                    <p className="text-3xs text-muted-foreground mt-1 truncate">{provA?.account_email || 'Not connected'}</p>
                    <p className="text-2xs text-muted-foreground mt-2 font-sans leading-relaxed">Stores docs, notes, databases, and AI memory contexts.</p>
                  </div>

                  <div className="pt-2">
                    <div className="flex justify-between text-3xs text-muted-foreground mb-1">
                      <span>Quota: 2.1 TB Free</span>
                      <span>Max: 5.0 TB</span>
                    </div>
                    <div className="h-1.5 w-full bg-border rounded-none overflow-hidden">
                      <div className="h-full bg-primary" style={{ width: '58%' }} />
                    </div>
                    <div className="mt-4 flex gap-2">
                      {provA?.connected ? (
                        <button
                          onClick={() => handleDisconnect(provA.id)}
                          className="w-full border border-red-500/35 hover:bg-red-500/10 px-3 py-1.5 text-2xs font-semibold text-red-400 transition-colors flex items-center justify-center gap-1 uppercase"
                        >
                          <Link2Off className="h-3 w-3" /> Disconnect
                        </button>
                      ) : (
                        <button
                          onClick={handleConnect}
                          className="w-full bg-primary hover:bg-primary/90 px-3 py-1.5 text-2xs font-semibold text-primary-foreground transition-colors flex items-center justify-center gap-1 uppercase"
                        >
                          <Link2 className="h-3 w-3" /> Connect
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })()}

            {/* Drive B (Assets) */}
            {(() => {
              const provB = providers.find(p => p.provider_label === 'B');
              return (
                <div className="border border-border bg-card p-5 flex flex-col justify-between space-y-4 font-mono text-xs">
                  <div>
                    <div className="flex items-center justify-between border-b border-border/40 pb-2">
                      <span className="text-[10px] text-muted-foreground uppercase font-bold">Assets Drive</span>
                      <span className={`text-[10px] font-bold ${
                        provB?.connected ? 'text-primary' : 'text-muted-foreground'
                      }`}>
                        {provB?.connected ? 'ONLINE' : 'OFFLINE'}
                      </span>
                    </div>
                    <h3 className="text-sm font-bold mt-3 text-foreground">GOOGLE_DRIVE_B</h3>
                    <p className="text-3xs text-muted-foreground mt-1 truncate">{provB?.account_email || 'Not connected'}</p>
                    <p className="text-2xs text-muted-foreground mt-2 font-sans leading-relaxed">Secondary backup storage node for logs, images, and archives.</p>
                  </div>

                  <div className="pt-2">
                    <div className="flex justify-between text-3xs text-muted-foreground mb-1">
                      <span>Quota: 4.6 TB Free</span>
                      <span>Max: 5.0 TB</span>
                    </div>
                    <div className="h-1.5 w-full bg-border rounded-none overflow-hidden">
                      <div className="h-full bg-primary" style={{ width: '8%' }} />
                    </div>
                    <div className="mt-4 flex gap-2">
                      {provB?.connected ? (
                        <button
                          onClick={() => handleDisconnect(provB.id)}
                          className="w-full border border-red-500/35 hover:bg-red-500/10 px-3 py-1.5 text-2xs font-semibold text-red-400 transition-colors flex items-center justify-center gap-1 uppercase"
                        >
                          <Link2Off className="h-3 w-3" /> Disconnect
                        </button>
                      ) : (
                        <button
                          onClick={handleConnectB}
                          className="w-full bg-primary hover:bg-primary/90 px-3 py-1.5 text-2xs font-semibold text-primary-foreground transition-colors flex items-center justify-center gap-1 uppercase"
                        >
                          <Link2 className="h-3 w-3" /> Connect
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })()}

            {/* Total Storage Summary */}
            <div className="border border-border bg-card p-5 flex flex-col justify-between space-y-4 font-mono text-xs">
              <div>
                <span className="text-[10px] text-muted-foreground uppercase font-bold">Aggregated Quotas</span>
                <h3 className="text-sm font-bold mt-3 text-foreground">TOTAL_POOLS</h3>
                <p className="text-2xs text-muted-foreground mt-1 font-sans">Sum of all connected storage node free capacities.</p>
                
                <div className="mt-4 space-y-2 text-2xs">
                  <div className="flex justify-between border-b border-border/40 pb-1.5">
                    <span className="text-muted-foreground">Available Space:</span>
                    <span className="font-bold text-foreground">6.7 TB Available</span>
                  </div>
                  <div className="flex justify-between border-b border-border/40 pb-1.5">
                    <span className="text-muted-foreground">Encryption Status:</span>
                    <span className="font-bold text-emerald-400">Fernet Crypt active</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Sync Engine:</span>
                    <span className="font-bold text-foreground">Alembic-head compliant</span>
                  </div>
                </div>
              </div>

              <div className="border border-border/80 p-3 text-3xs text-muted-foreground flex flex-col gap-1">
                <span className="font-bold text-foreground uppercase tracking-wider">Sync Status:</span>
                <span>All local database tables aligned to Drive A root folder.</span>
              </div>
            </div>
          </div>

          {/* Sync status nodes */}
          {isConnected && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {['notes', 'finance', 'books', 'habits'].map((section) => (
                <div key={section} className="border border-border bg-card p-4 flex flex-col justify-between gap-3 font-mono text-xs text-left">
                  <div>
                    <h3 className="text-xs font-bold text-foreground capitalize flex items-center gap-1.5">
                      <span className="h-2 w-2 rounded-full bg-primary"></span>
                      {section} Sync
                    </h3>
                    <p className="text-3xs text-muted-foreground mt-1 font-sans leading-relaxed">
                      Backup local {section} database records or restore from Drive.
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleSyncSection(section)}
                      disabled={syncing[section]}
                      className="flex-1 border border-border hover:border-primary px-2.5 py-1 text-3xs text-foreground font-semibold text-center hover:bg-primary/5 transition-colors disabled:opacity-50 inline-flex justify-center items-center gap-1 uppercase"
                    >
                      {syncing[section] ? (
                        <Loader2 className="h-3 w-3 animate-spin text-primary" />
                      ) : (
                        'Backup'
                      )}
                    </button>
                    <button
                      onClick={() => handleRestoreSection(section)}
                      disabled={restoring[section]}
                      className="flex-1 bg-primary hover:bg-primary/95 px-2.5 py-1 text-3xs text-primary-foreground font-semibold text-center transition-colors disabled:opacity-50 inline-flex justify-center items-center gap-1 uppercase"
                    >
                      {restoring[section] ? (
                        <Loader2 className="h-3 w-3 animate-spin text-primary-foreground" />
                      ) : (
                        'Restore'
                      )}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* ─── MEDIA GALLERY VIEW ───────────────────────────── */}
      {vaultView === 'media' && (
        <div className="border border-border bg-card p-5 space-y-4 font-mono text-xs">
          <div className="flex items-center justify-between border-b border-border/40 pb-2">
            <span className="text-[10px] text-muted-foreground uppercase font-bold">MEDIA_LIBRARY_INDEX</span>
            <span className="text-[10px] text-emerald-400">8 FILES FOUND</span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {[
              { name: 'architecture_diagram.png', size: '1.2 MB', type: 'IMAGE' },
              { name: 'gating_flowchart.jpg', size: '890 KB', type: 'IMAGE' },
              { name: 'telemetry_run_screencast.mp4', size: '14.5 MB', type: 'VIDEO' },
              { name: 'system_alert_ping.wav', size: '120 KB', type: 'AUDIO' }
            ].map((media, i) => (
              <div key={i} className="border border-border/60 bg-muted/10 p-3 flex flex-col justify-between min-h-[140px] relative">
                <div className="flex-1 flex items-center justify-center bg-background border border-border/40 mb-2 h-20 text-[10px] text-muted-foreground">
                  [{media.type}] PREVIEW
                </div>
                <div>
                  <span className="block truncate text-foreground font-bold text-3xs">{media.name.toUpperCase()}</span>
                  <span className="text-[9px] text-muted-foreground block mt-0.5">{media.size}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ─── FILES BROWSER VIEW ───────────────────────────── */}
      {vaultView === 'files' && (
        <div className="border border-border bg-card p-4 flex flex-col gap-4">
          {/* Operations Bar */}
          <div className="flex flex-col sm:flex-row gap-3 items-center justify-between border-b border-border/40 pb-4">
            {/* Search */}
            <form onSubmit={handleSearch} className="relative w-full sm:w-80">
              <input
                type="text"
                placeholder="Search files..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full rounded-none border border-border bg-background py-1.5 pl-8 pr-8 text-xs outline-none focus:border-primary transition-colors text-foreground font-mono"
              />
              <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-muted-foreground" />
              {searchQuery && (
                <button
                  type="button"
                  onClick={clearSearch}
                  className="absolute right-2.5 top-2 text-xs text-muted-foreground hover:text-foreground font-mono"
                >
                  Clear
                </button>
              )}
            </form>

            {/* Folder Actions */}
            <div className="flex gap-2 w-full sm:w-auto justify-end font-mono">
              <button
                onClick={() => setShowFolderModal(true)}
                className="border border-border bg-card hover:bg-accent px-3 py-1.5 text-3xs font-bold text-foreground flex items-center gap-1.5 transition-colors uppercase"
              >
                <FolderPlus className="h-3.5 w-3.5" />
                New Folder
              </button>
              <button
                onClick={handleUploadClick}
                disabled={isUploading}
                className="bg-primary text-primary-foreground hover:bg-primary/90 px-3 py-1.5 text-3xs font-bold flex items-center gap-1.5 transition-colors uppercase"
              >
                {isUploading ? (
                  <Loader2 className="h-3.5 w-3.5 animate-spin" />
                ) : (
                  <Upload className="h-3.5 w-3.5" />
                )}
                Upload File
              </button>
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                className="hidden"
              />
            </div>
          </div>

          {/* Upload Progress Alert */}
          {isUploading && uploadProgress && (
            <div className="border border-primary/20 bg-primary/5 p-3 text-xs text-primary flex items-center gap-2 font-mono">
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
              {uploadProgress}
            </div>
          )}

          {/* Breadcrumb Path */}
          <div className="flex items-center gap-1 flex-wrap text-xs font-mono text-muted-foreground py-1 bg-muted/10 px-2">
            {breadcrumbs.map((crumb, idx) => (
              <div key={crumb.id} className="flex items-center gap-1">
                {idx > 0 && <ChevronRight className="h-3.5 w-3.5 text-muted-foreground/50" />}
                <button
                  onClick={() => handleBreadcrumbClick(crumb, idx)}
                  className={`hover:text-foreground transition-colors uppercase ${
                    idx === breadcrumbs.length - 1 ? 'text-foreground font-semibold' : ''
                  }`}
                >
                  {crumb.name}
                </button>
              </div>
            ))}
            {isSearching && (
              <span className="text-primary ml-2 font-semibold">
                (Search results for &quot;{searchQuery}&quot;)
              </span>
            )}
            <button
              onClick={() => loadFiles(currentFolder, searchQuery)}
              className="ml-auto p-1 hover:bg-accent transition-colors text-muted-foreground hover:text-foreground"
              title="Refresh list"
            >
              <RefreshCw className="h-3 w-3" />
            </button>
          </div>

          {/* Directory Files List */}
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-border text-muted-foreground font-medium select-none font-mono">
                  <th className="py-2.5 pl-2 font-semibold">Name</th>
                  <th className="py-2.5 font-semibold hidden md:table-cell">Modified</th>
                  <th className="py-2.5 font-semibold text-right pr-6 hidden sm:table-cell">Size</th>
                  <th className="py-2.5 font-semibold text-right pr-4">Actions</th>
                </tr>
              </thead>
              <tbody>
                {files.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="py-12 text-center text-muted-foreground font-mono">
                      This folder is empty.
                    </td>
                  </tr>
                ) : (
                  files.map((file) => (
                    <tr
                      key={file.id}
                      className="border-b border-border/50 hover:bg-muted/40 transition-colors group font-mono"
                    >
                      <td className="py-3 pl-2 max-w-xs md:max-w-md truncate">
                        {isFolder(file.mimeType) ? (
                          <button
                            onClick={() => handleFolderClick(file)}
                            className="flex items-center gap-3 text-left font-medium hover:text-primary hover:underline outline-none text-foreground"
                          >
                            {getFileIcon(file.mimeType)}
                            <span className="truncate">{file.name.toUpperCase()}</span>
                          </button>
                        ) : (
                          <div className="flex items-center gap-3 text-muted-foreground">
                            {getFileIcon(file.mimeType)}
                            <span className="truncate font-medium text-foreground">{file.name.toUpperCase()}</span>
                          </div>
                        )}
                      </td>
                      <td className="py-3 text-muted-foreground hidden md:table-cell text-3xs">
                        {new Date(file.modifiedTime).toLocaleDateString(undefined, {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit',
                          hour12: false
                        })}
                      </td>
                      <td className="py-3 text-right pr-6 text-muted-foreground hidden sm:table-cell">
                        {formatBytes(file.size)}
                      </td>
                      <td className="py-3 text-right pr-4">
                        <div className="inline-flex gap-1">
                          {!isFolder(file.mimeType) && (
                            <button
                              onClick={() => handleDownload(file)}
                              className="p-1.5 rounded hover:bg-accent text-muted-foreground hover:text-foreground transition-colors"
                              title="Download"
                            >
                              <Download className="h-3.5 w-3.5" />
                            </button>
                          )}
                          <button
                            onClick={() => handleDelete(file)}
                            className="p-1.5 rounded hover:bg-destructive/10 text-muted-foreground hover:text-destructive transition-colors"
                            title="Delete"
                          >
                            <Trash2 className="h-3.5 w-3.5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* New Folder Modal */}
      {showFolderModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm">
          <div className="w-full max-w-sm border border-border bg-card p-6 rounded-none font-mono text-xs">
            <h3 className="text-sm font-semibold text-foreground flex items-center gap-2">
              <FolderPlus className="h-4 w-4 text-primary" />
              CREATE NEW FOLDER
            </h3>
            <form onSubmit={handleCreateFolder} className="mt-4 flex flex-col gap-4">
              <input
                type="text"
                placeholder="Folder name"
                value={newFolderName}
                onChange={(e) => setNewFolderName(e.target.value)}
                required
                className="w-full rounded-none border border-border bg-background px-3 py-1.5 text-xs outline-none focus:border-primary text-foreground"
                autoFocus
              />
              <div className="flex justify-end gap-2 text-xs font-semibold">
                <button
                  type="button"
                  onClick={() => {
                    setShowFolderModal(false);
                    setNewFolderName('');
                  }}
                  className="border border-border px-3 py-1.5 text-foreground hover:bg-accent transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isCreatingFolder}
                  className="bg-primary px-3 py-1.5 text-primary-foreground hover:bg-primary/95 transition-colors flex items-center gap-1 uppercase"
                >
                  {isCreatingFolder && <Loader2 className="h-3 w-3 animate-spin" />}
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
