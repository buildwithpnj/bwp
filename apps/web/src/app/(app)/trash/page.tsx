'use client';

import { Trash2, ShieldAlert, RefreshCw } from 'lucide-react';

export default function TrashPage() {
  return (
    <div className="space-y-6 animate-fade-in text-foreground">
      {/* System Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">System Cleanup</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <Trash2 className="h-7 w-7 text-primary" />
            Trash & Archives
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Recover or permanently delete files, documents, and historical notes.
          </p>
        </div>
      </div>

      {/* Main Container */}
      <div className="rounded-2xl border border-border bg-card/30 p-8 flex flex-col items-center justify-center text-center max-w-xl mx-auto min-h-[40vh] space-y-4">
        <div className="rounded-full bg-primary/10 p-4">
          <ShieldAlert className="h-10 w-10 text-primary" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-foreground">Trash bin is empty</h3>
          <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
            When you delete files or notes inside Warborn OS, they will be archived here for up to 30 days before permanent automatic purging.
          </p>
        </div>
      </div>
    </div>
  );
}
