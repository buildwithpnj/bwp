'use client';

import { X, UploadCloud, Check, AlertCircle, Trash2, Loader2, HardDrive } from 'lucide-react';
import { useUploadCenter, PendingUploadFile } from '@/hooks/use-upload-center';
import { getAccessToken } from '@/lib/api';

export function UploadCenter() {
  const {
    isOpen,
    files,
    setOpen,
    removeFile,
    updateFileCategory,
    updateFileDestination,
    startUploads,
    clear,
  } = useUploadCenter();

  if (!isOpen) return null;

  const categories: PendingUploadFile['detectedCategory'][] = [
    'assets',
    'books',
    'notes',
    'media',
    'archives',
    'projects',
  ];

  const handleUploadAll = async () => {
    const token = getAccessToken();
    await startUploads(token);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md p-4 animate-fade-in">
      <div className="w-full max-w-2xl rounded-2xl border border-border bg-card/90 backdrop-blur-lg shadow-2xl overflow-hidden flex flex-col max-h-[85vh]">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-border px-6 py-4 bg-muted/40">
          <div>
            <h2 className="text-base font-bold tracking-tight text-foreground flex items-center gap-2">
              <UploadCloud className="h-5 w-5 text-primary" />
              Unified Upload Center
            </h2>
            <p className="text-xs text-muted-foreground mt-0.5">
              Refined file routing, classification, and target destination override.
            </p>
          </div>
          <button
            onClick={() => setOpen(false)}
            className="rounded-lg p-1.5 text-muted-foreground hover:bg-accent hover:text-foreground transition-colors"
          >
            <X className="h-4.5 w-4.5" />
          </button>
        </div>

        {/* File List */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {files.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="rounded-full bg-primary/10 p-4 mb-3">
                <UploadCloud className="h-8 w-8 text-primary" />
              </div>
              <p className="text-sm font-semibold text-foreground">No files in queue</p>
              <p className="text-xs text-muted-foreground mt-1">
                Drag & drop files onto the operating system workspace to add them.
              </p>
            </div>
          ) : (
            files.map((item, index) => (
              <div
                key={index}
                className="relative rounded-xl border border-border bg-card/50 p-4 space-y-3 transition-all hover:border-primary/20"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0 flex-1">
                    <p className="text-xs font-semibold text-foreground truncate">{item.file.name}</p>
                    <p className="text-3xs text-muted-foreground mt-0.5">
                      {(item.file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                  <button
                    onClick={() => removeFile(index)}
                    className="text-muted-foreground hover:text-destructive p-1 rounded transition-colors"
                    disabled={item.status === 'uploading'}
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </button>
                </div>

                {/* Classification and Target Drive Controls */}
                <div className="flex flex-wrap items-center gap-3 pt-1">
                  {/* Category Classification Selector */}
                  <div className="flex items-center gap-1.5">
                    <span className="text-3xs font-bold uppercase tracking-wider text-muted-foreground">Class:</span>
                    <select
                      value={item.detectedCategory}
                      onChange={(e) =>
                        updateFileCategory(
                          index,
                          e.target.value as PendingUploadFile['detectedCategory']
                        )
                      }
                      className="rounded border border-border bg-background px-2 py-0.5 text-2xs text-foreground focus:border-primary focus:outline-none"
                      disabled={item.status === 'uploading'}
                    >
                      {categories.map((cat) => (
                        <option key={cat} value={cat}>
                          {cat.toUpperCase()}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Provider Destination Target Selector */}
                  <div className="flex items-center gap-1.5">
                    <span className="text-3xs font-bold uppercase tracking-wider text-muted-foreground">Target:</span>
                    <select
                      value={item.destination}
                      onChange={(e) =>
                        updateFileDestination(index, e.target.value as PendingUploadFile['destination'])
                      }
                      className="rounded border border-border bg-background px-2 py-0.5 text-2xs text-foreground focus:border-primary focus:outline-none"
                      disabled={item.status === 'uploading'}
                    >
                      <option value="A">Primary Drive (A)</option>
                      <option value="B">Assets Drive (B)</option>
                    </select>
                  </div>

                  {/* Status Banner */}
                  <div className="ml-auto flex items-center gap-1.5 text-3xs font-medium">
                    {item.status === 'pending' && (
                      <span className="text-amber-400 font-semibold uppercase tracking-wider">Ready</span>
                    )}
                    {item.status === 'uploading' && (
                      <span className="text-blue-400 font-semibold uppercase tracking-wider flex items-center gap-1">
                        <Loader2 className="h-3 w-3 animate-spin" /> Uploading {item.progress}%
                      </span>
                    )}
                    {item.status === 'success' && (
                      <span className="text-emerald-400 font-semibold uppercase tracking-wider flex items-center gap-1">
                        <Check className="h-3 w-3" /> Complete
                      </span>
                    )}
                    {item.status === 'error' && (
                      <span className="text-destructive font-semibold uppercase tracking-wider flex items-center gap-1">
                        <AlertCircle className="h-3 w-3" /> Error
                      </span>
                    )}
                  </div>
                </div>

                {/* Progress bar */}
                {item.status === 'uploading' && (
                  <div className="h-1 w-full bg-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary transition-all duration-300"
                      style={{ width: `${item.progress}%` }}
                    />
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {/* Footer actions */}
        <div className="border-t border-border px-6 py-4 bg-muted/20 flex justify-end gap-3">
          <button
            onClick={clear}
            className="rounded-lg border border-border px-4 py-2 text-xs font-semibold text-muted-foreground hover:bg-accent hover:text-foreground transition-all"
          >
            Clear All
          </button>
          <button
            onClick={handleUploadAll}
            disabled={files.length === 0 || files.every((f) => f.status === 'success')}
            className="rounded-lg bg-primary px-5 py-2 text-xs font-semibold text-primary-foreground hover:bg-primary/90 disabled:opacity-50 transition-all flex items-center gap-1.5"
          >
            {files.some((f) => f.status === 'uploading') ? (
              <>
                <Loader2 className="h-3.5 w-3.5 animate-spin" /> Uploading...
              </>
            ) : (
              'Start Uploads'
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
