'use client';

import { useState, useEffect } from 'react';
import { Image as ImageIcon, Search, Download, Trash2, Loader2, HardDrive, RefreshCw } from 'lucide-react';
import { api, getAccessToken } from '@/lib/api';

interface AssetFile {
  id: string;
  name: string;
  mimeType: string;
  size?: string;
  modifiedTime: string;
  thumbnailLink?: string;
  provider_id?: string;
}

export default function AssetsExplorerPage() {
  const [assets, setAssets] = useState<AssetFile[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  const loadAssets = async () => {
    setLoading(true);
    try {
      // Query files using the multi-provider list, filtering by images
      const res = await api<{ files: AssetFile[] }>('/api/storage/list?folder_id=root');
      const filtered = (res.files || []).filter(
        (f) => f.mimeType.startsWith('image/') || f.mimeType.startsWith('video/')
      );
      setAssets(filtered);
    } catch (err) {
      console.error('Failed to load assets in Explorer:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAssets();
  }, []);

  const handleDownload = async (file: AssetFile) => {
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
      alert('Failed to download asset.');
      console.error(err);
    }
  };

  const handleDelete = async (file: AssetFile) => {
    if (confirm(`Delete asset "${file.name}"?`)) {
      try {
        const providerQuery = file.provider_id ? `?provider_id=${file.provider_id}` : '';
        await api(`/api/storage/delete/${file.id}${providerQuery}`, { method: 'DELETE' });
        await loadAssets();
      } catch (err) {
        alert('Failed to delete asset.');
        console.error(err);
      }
    }
  };

  return (
    <div className="space-y-6 animate-fade-in text-foreground h-[calc(100vh-80px)] overflow-hidden flex flex-col">
      {/* System Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">Media Library</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <ImageIcon className="h-7 w-7 text-primary" />
            Asset Explorer
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Overview of uploaded images, screenshots, vectors, and layouts inside Google Drive B.
          </p>
        </div>

        {/* Search */}
        <div className="flex items-center gap-3">
          <div className="relative w-full sm:w-60">
            <input
              type="text"
              placeholder="Search assets..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-md border border-border bg-background py-1.5 pl-8 pr-3 text-xs outline-none focus:border-primary text-foreground"
            />
            <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-muted-foreground" />
          </div>
          <button
            onClick={loadAssets}
            className="p-2 hover:bg-accent rounded-lg border border-border transition-colors text-muted-foreground hover:text-foreground"
            title="Refresh assets"
          >
            <RefreshCw className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

      {/* Grid of assets */}
      <div className="flex-1 overflow-y-auto pb-12 pr-2">
        {loading ? (
          <div className="flex h-[40vh] items-center justify-center">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        ) : assets.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-center text-muted-foreground">
            <ImageIcon className="h-12 w-12 mb-3 text-muted-foreground/35" />
            <p className="text-sm font-semibold">No assets found</p>
            <p className="text-xs mt-1">Drag and drop images onto the layout to upload them directly to Drive B.</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 gap-4">
            {assets
              .filter((f) => f.name.toLowerCase().includes(searchQuery.toLowerCase()))
              .map((file) => (
                <div
                  key={file.id}
                  className="group relative rounded-xl border border-border bg-card/45 p-2 flex flex-col justify-between hover:border-primary/20 transition-all hover:-translate-y-0.5 shadow-sm"
                >
                  {/* Thumbnail / Image container */}
                  <div className="aspect-square bg-muted rounded-lg border border-border overflow-hidden flex items-center justify-center relative">
                    {file.thumbnailLink ? (
                      <img src={file.thumbnailLink} alt="" className="w-full h-full object-cover" />
                    ) : (
                      <ImageIcon className="h-8 w-8 text-muted-foreground/30" />
                    )}

                    {/* Action hover triggers */}
                    <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 flex items-center justify-center gap-2 transition-opacity duration-200">
                      <button
                        onClick={() => handleDownload(file)}
                        className="p-1.5 rounded bg-card/95 border border-border hover:text-primary transition-all shadow-sm scale-90 hover:scale-100"
                        title="Download file"
                      >
                        <Download className="h-3.5 w-3.5" />
                      </button>
                      <button
                        onClick={() => handleDelete(file)}
                        className="p-1.5 rounded bg-card/95 border border-border hover:text-destructive transition-all shadow-sm scale-90 hover:scale-100"
                        title="Delete file"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  </div>

                  {/* metadata details */}
                  <div className="pt-2 px-1">
                    <p className="text-3xs font-semibold truncate text-foreground leading-tight" title={file.name}>
                      {file.name}
                    </p>
                    <div className="flex items-center justify-between text-4xs text-muted-foreground mt-1">
                      <span>{new Date(file.modifiedTime).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );
}
