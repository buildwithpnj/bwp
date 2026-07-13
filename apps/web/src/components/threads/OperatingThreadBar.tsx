'use client';

import { useOperatingThreads } from '@/hooks/useOperatingThreads';
import { useState } from 'react';

export function OperatingThreadBar() {
  const { activeThread, createThread, transitionThread } = useOperatingThreads();
  const [newTitle, setNewTitle] = useState('');
  const [showInput, setShowInput] = useState(false);

  const handleStart = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    await createThread(newTitle, 'Custom workflow thread');
    setNewTitle('');
    setShowInput(false);
  };

  return (
    <div className="flex h-10 items-center justify-between border-b border-border bg-muted/20 px-4 text-xs">
      <div className="flex items-center gap-2">
        <span className="font-semibold text-muted-foreground uppercase text-[10px]">Active Thread:</span>
        {activeThread ? (
          <div className="flex items-center gap-2">
            <span className="font-medium text-foreground">{activeThread.title}</span>
            <button
              onClick={() => transitionThread(activeThread.id, 'paused')}
              className="text-amber-400 hover:text-amber-300 text-[10px] underline"
            >
              Pause
            </button>
          </div>
        ) : (
          <span className="text-muted-foreground italic">No focus thread active.</span>
        )}
      </div>

      <div>
        {showInput ? (
          <form onSubmit={handleStart} className="flex gap-2">
            <input
              type="text"
              value={newTitle}
              onChange={e => setNewTitle(e.target.value)}
              placeholder="Thread name..."
              className="bg-background border border-border px-2 py-0.5 rounded text-[10px] text-foreground focus:outline-none"
            />
            <button
              type="submit"
              className="bg-primary text-primary-foreground px-2 py-0.5 rounded text-[10px] font-semibold"
            >
              Start
            </button>
          </form>
        ) : (
          <button
            onClick={() => setShowInput(true)}
            className="text-primary hover:text-primary/95 text-[10px] underline font-medium"
          >
            + New Thread Focus
          </button>
        )}
      </div>
    </div>
  );
}
export default OperatingThreadBar;
