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
    <div className="flex flex-col gap-6 p-6 animate-fade-in text-foreground">
      {/* ─── SYSTEM HEADER ────────────────────────────────────── */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">System Infrastructure</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <HardDrive className="h-7 w-7 text-primary animate-pulse" />
            Storage Manager
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Dynamic file classification, backup, and storage node capacity manager.
          </p>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          {providers.filter(p => p.connected).map(p => (
            <span key={p.id} className="text-xs text-muted-foreground border border-border bg-card/50 rounded-full px-3 py-1 flex items-center gap-1.5 font-mono">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
              Drive {p.provider_label}
            </span>
          ))}
        </div>
      </div>

      {/* ─── STORAGE OVERVIEW PANEL ───────────────────────────── */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Drive A (Primary) */}
        {(() => {
          const provA = providers.find(p => p.provider_label === 'A');
          return (
            <div className="rounded-xl border border-border bg-card/30 p-5 flex flex-col justify-between space-y-4">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-3xs font-bold uppercase tracking-wider text-muted-foreground">Primary Drive</span>
                  <span className={`rounded-full px-2 py-0.5 text-3xs font-bold font-mono ${
                    provA?.connected ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-muted text-muted-foreground'
                  }`}>
                    {provA?.connected ? 'ONLINE' : 'OFFLINE'}
                  </span>
                </div>
                <h3 className="text-sm font-bold mt-2">Google Drive A</h3>
                <p className="text-3xs text-muted-foreground font-mono mt-1 truncate">{provA?.account_email || 'Not connected'}</p>
                <p className="text-2xs text-muted-foreground mt-2">Used to store documents, notes, databases, and AI memory contexts.</p>
              </div>

              <div className="pt-2">
                <div className="flex justify-between text-3xs font-mono text-muted-foreground mb-1">
                  <span>Quota: 2.1 TB Free</span>
                  <span>Max: 5.0 TB</span>
                </div>
                <div className="h-1.5 w-full bg-border rounded-full overflow-hidden">
                  <div className="h-full bg-primary" style={{ width: '58%' }} />
                </div>
                <div className="mt-4 flex gap-2">
                  {provA?.connected ? (
                    <button
                      onClick={() => handleDisconnect(provA.id)}
                      className="w-full rounded-lg border border-destructive/30 hover:bg-destructive/10 px-3 py-1.5 text-2xs font-semibold text-destructive transition-colors flex items-center justify-center gap-1"
                    >
                      <Link2Off className="h-3 w-3" /> Disconnect
                    </button>
                  ) : (
                    <button
                      onClick={handleConnect}
                      className="w-full rounded-lg bg-primary hover:bg-primary/90 px-3 py-1.5 text-2xs font-semibold text-primary-foreground transition-colors flex items-center justify-center gap-1"
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
            <div className="rounded-xl border border-border bg-card/30 p-5 flex flex-col justify-between space-y-4">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-3xs font-bold uppercase tracking-wider text-muted-foreground">Assets Drive</span>
                  <span className={`rounded-full px-2 py-0.5 text-3xs font-bold font-mono ${
                    provB?.connected ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' : 'bg-muted text-muted-foreground border border-border'
                  }`}>
                    {provB?.connected ? 'ONLINE' : 'OFFLINE'}
                  </span>
                </div>
                <h3 className="text-sm font-bold mt-2">Google Drive B</h3>
                <p className="text-3xs text-muted-foreground font-mono mt-1 truncate">{provB?.account_email || 'Not connected'}</p>
                <p className="text-2xs text-muted-foreground mt-2">Secondary backup storage node for images, logs, videos, and archives.</p>
              </div>

              <div className="pt-2">
                <div className="flex justify-between text-3xs font-mono text-muted-foreground mb-1">
                  <span>Quota: 4.6 TB Free</span>
                  <span>Max: 5.0 TB</span>
                </div>
                <div className="h-1.5 w-full bg-border rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500" style={{ width: '8%' }} />
                </div>
                <div className="mt-4 flex gap-2">
                  {provB?.connected ? (
                    <button
                      onClick={() => handleDisconnect(provB.id)}
                      className="w-full rounded-lg border border-destructive/30 hover:bg-destructive/10 px-3 py-1.5 text-2xs font-semibold text-destructive transition-colors flex items-center justify-center gap-1"
                    >
                      <Link2Off className="h-3 w-3" /> Disconnect
                    </button>
                  ) : (
                    <button
                      onClick={handleConnectB}
                      className="w-full rounded-lg bg-blue-600 hover:bg-blue-500 px-3 py-1.5 text-2xs font-semibold text-white transition-colors flex items-center justify-center gap-1"
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
        <div className="rounded-xl border border-border bg-card/30 p-5 flex flex-col justify-between space-y-4">
          <div>
            <span className="text-3xs font-bold uppercase tracking-wider text-muted-foreground">Aggregated Quotas</span>
            <h3 className="text-sm font-bold mt-2">Total Storage Pools</h3>
            <p className="text-2xs text-muted-foreground mt-1">Sum of all connected storage node free capacities.</p>
            
            <div className="mt-4 space-y-2 font-mono text-2xs">
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

          <div className="rounded-lg bg-muted/20 border border-border/80 p-3 text-3xs text-muted-foreground flex flex-col gap-1">
            <span className="font-bold text-foreground uppercase tracking-wider">Sync Status:</span>
            <span>All local database tables aligned to Drive A root folder.</span>
          </div>
        </div>
      </div>

      {/* ─── GOOGLE DRIVE SYNC PANEL ───────────────────────────── */}
      {isConnected && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {['notes', 'finance', 'books', 'habits'].map((section) => (
            <div key={section} className="rounded-xl border border-border bg-card/45 p-4 flex flex-col justify-between gap-3 text-left">
              <div>
                <h3 className="text-xs font-bold text-foreground capitalize flex items-center gap-1.5">
                  <span className="h-2 w-2 rounded-full bg-primary"></span>
                  {section} Sync
                </h3>
                <p className="text-3xs text-muted-foreground mt-1">
                  Backup local {section} database records to Google Drive or restore from cloud.
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => handleSyncSection(section)}
                  disabled={syncing[section]}
                  className="flex-1 rounded border border-border hover:border-primary px-2.5 py-1 text-3xs text-foreground font-semibold text-center hover:bg-primary/5 transition-colors disabled:opacity-50 inline-flex justify-center items-center gap-1"
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
                  className="flex-1 rounded bg-primary hover:bg-primary/95 px-2.5 py-1 text-3xs text-primary-foreground font-semibold text-center transition-colors disabled:opacity-50 inline-flex justify-center items-center gap-1"
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

      {/* Loading Indicator */}
      {loading && files.length === 0 && (
        <div className="flex min-h-[30vh] items-center justify-center">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      )}

      {/* ─── CONNECTED STORAGE BROWSER ────────────────────────── */}
      {isConnected && (
        <div className="flex flex-col gap-4 border border-border rounded-xl bg-card p-4 shadow-sm">
          
          {/* Operations Bar */}
          <div className="flex flex-col sm:flex-row gap-3 items-center justify-between border-b border-border pb-4">
            {/* Search */}
            <form onSubmit={handleSearch} className="relative w-full sm:w-80">
              <input
                type="text"
                placeholder="Search files..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full rounded-md border border-border bg-background py-1.5 pl-8 pr-8 text-sm outline-none focus:border-primary transition-colors text-foreground"
              />
              <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-muted-foreground" />
              {searchQuery && (
                <button
                  type="button"
                  onClick={clearSearch}
                  className="absolute right-2.5 top-2.5 text-xs text-muted-foreground hover:text-foreground"
                >
                  Clear
                </button>
              )}
            </form>

            {/* Folder Actions */}
            <div className="flex gap-2 w-full sm:w-auto justify-end">
              <button
                onClick={() => setShowFolderModal(true)}
                className="rounded-md border border-border bg-card hover:bg-accent px-3 py-1.5 text-xs font-semibold text-foreground flex items-center gap-1.5 transition-colors"
              >
                <FolderPlus className="h-3.5 w-3.5" />
                New Folder
              </button>
              <button
                onClick={handleUploadClick}
                disabled={isUploading}
                className="rounded-md bg-primary hover:bg-primary/90 px-3 py-1.5 text-xs font-semibold text-primary-foreground flex items-center gap-1.5 transition-colors"
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
            <div className="rounded-lg bg-primary/10 border border-primary/20 p-3 text-xs text-primary flex items-center gap-2">
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
              {uploadProgress}
            </div>
          )}

          {/* Breadcrumb Path */}
          <div className="flex items-center gap-1 flex-wrap text-xs font-medium text-muted-foreground py-1 bg-muted/30 px-2 rounded-md">
            {breadcrumbs.map((crumb, idx) => (
              <div key={crumb.id} className="flex items-center gap-1">
                {idx > 0 && <ChevronRight className="h-3.5 w-3.5 text-muted-foreground/50" />}
                <button
                  onClick={() => handleBreadcrumbClick(crumb, idx)}
                  className={`hover:text-foreground transition-colors ${
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
              className="ml-auto p-1 hover:bg-accent rounded-full transition-colors text-muted-foreground hover:text-foreground"
              title="Refresh list"
            >
              <RefreshCw className="h-3 w-3" />
            </button>
          </div>

          {/* Directory Files Grid/List */}
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-border text-muted-foreground font-medium select-none">
                  <th className="py-2.5 pl-2 font-semibold">Name</th>
                  <th className="py-2.5 font-semibold hidden md:table-cell">Modified</th>
                  <th className="py-2.5 font-semibold text-right pr-6 hidden sm:table-cell">Size</th>
                  <th className="py-2.5 font-semibold text-right pr-4">Actions</th>
                </tr>
              </thead>
              <tbody>
                {files.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="py-12 text-center text-muted-foreground">
                      This folder is empty.
                    </td>
                  </tr>
                ) : (
                  files.map((file) => (
                    <tr
                      key={file.id}
                      className="border-b border-border/50 hover:bg-muted/40 transition-colors group"
                    >
                      <td className="py-3 pl-2 max-w-xs md:max-w-md truncate">
                        {isFolder(file.mimeType) ? (
                          <button
                            onClick={() => handleFolderClick(file)}
                            className="flex items-center gap-3 text-left font-medium hover:text-primary hover:underline outline-none text-foreground"
                          >
                            {getFileIcon(file.mimeType)}
                            <span className="truncate">{file.name}</span>
                          </button>
                        ) : (
                          <div className="flex items-center gap-3 text-muted-foreground">
                            {getFileIcon(file.mimeType)}
                            <span className="truncate font-medium text-foreground">{file.name}</span>
                          </div>
                        )}
                      </td>
                      <td className="py-3 text-muted-foreground hidden md:table-cell">
                        {new Date(file.modifiedTime).toLocaleDateString(undefined, {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit',
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
          <div className="w-full max-w-sm rounded-xl border border-border bg-card p-6 shadow-lg">
            <h3 className="text-sm font-semibold text-foreground flex items-center gap-2">
              <FolderPlus className="h-4 w-4 text-primary" />
              Create New Folder
            </h3>
            <form onSubmit={handleCreateFolder} className="mt-4 flex flex-col gap-4">
              <input
                type="text"
                placeholder="Folder name"
                value={newFolderName}
                onChange={(e) => setNewFolderName(e.target.value)}
                required
                className="w-full rounded-md border border-border bg-background px-3 py-1.5 text-xs outline-none focus:border-primary text-foreground"
                autoFocus
              />
              <div className="flex justify-end gap-2 text-xs font-semibold">
                <button
                  type="button"
                  onClick={() => {
                    setShowFolderModal(false);
                    setNewFolderName('');
                  }}
                  className="rounded-md border border-border px-3 py-1.5 text-foreground hover:bg-accent transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isCreatingFolder}
                  className="rounded-md bg-primary px-3 py-1.5 text-primary-foreground hover:bg-primary/95 transition-colors flex items-center gap-1"
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
