'use client';

import { useOperatingThreads } from '@/hooks/useOperatingThreads';
import { ThreadSummaryCard } from './ThreadSummaryCard';

export function ThreadResumePanel() {
  const { threads, transitionThread } = useOperatingThreads();

  return (
    <div className="bg-background border border-border p-4 rounded-xl space-y-4">
      <div className="border-b border-border pb-2 flex items-center justify-between">
        <h3 className="font-semibold text-foreground text-xs">Continuity Threads Workspace</h3>
        <span className="text-[10px] text-muted-foreground">{threads.length} total</span>
      </div>

      <div className="space-y-3 max-h-60 overflow-y-auto">
        {threads.length === 0 ? (
          <p className="text-[10px] text-muted-foreground text-center py-4">
            No operating threads created yet. Start a focus above.
          </p>
        ) : (
          threads.map(thread => (
            <ThreadSummaryCard
              key={thread.id}
              thread={thread}
              onActivate={(id) => transitionThread(id, 'active')}
            />
          ))
        )}
      </div>
    </div>
  );
}
export default ThreadResumePanel;
