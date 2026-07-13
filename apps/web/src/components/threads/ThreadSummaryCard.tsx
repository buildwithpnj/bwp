'use client';

import { OperatingThread } from '@/hooks/useOperatingThreads';

interface ThreadSummaryCardProps {
  thread: OperatingThread;
  onActivate: (id: string) => void;
}

export function ThreadSummaryCard({ thread, onActivate }: ThreadSummaryCardProps) {
  return (
    <div className="p-3 bg-muted/40 border border-border rounded-lg flex flex-col gap-1.5 text-left">
      <div className="flex items-center justify-between">
        <h4 className="font-semibold text-foreground text-xs">{thread.title}</h4>
        <span className="text-[9px] uppercase px-1.5 py-0.5 rounded bg-muted text-muted-foreground font-medium">
          {thread.status}
        </span>
      </div>
      {thread.description && (
        <p className="text-[10px] text-muted-foreground leading-normal">
          {thread.description}
        </p>
      )}
      {thread.status !== 'active' && (
        <button
          onClick={() => onActivate(thread.id)}
          className="text-primary hover:text-primary/90 text-[10px] font-semibold text-left underline"
        >
          Resume Focus Thread
        </button>
      )}
    </div>
  );
}
