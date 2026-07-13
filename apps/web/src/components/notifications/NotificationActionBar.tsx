'use client';

import { useNotificationActions } from '@/hooks/useNotificationActions';
import { useState } from 'react';

interface NotificationActionBarProps {
  notificationId: string;
  sourceType: string;
  onActionComplete: () => void;
}

export function NotificationActionBar({
  notificationId,
  sourceType,
  onActionComplete
}: NotificationActionBarProps) {
  const { triggerAction } = useNotificationActions();
  const [isRunning, setIsRunning] = useState(false);

  const handleAction = async (type: string) => {
    setIsRunning(true);
    const success = await triggerAction(notificationId, type);
    setIsRunning(false);
    if (success) {
      onActionComplete();
    }
  };

  return (
    <div className="flex gap-2.5 pt-1.5 border-t border-border/10 mt-2">
      <button
        onClick={() => handleAction('approve')}
        disabled={isRunning}
        className="bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 px-2 py-0.5 rounded text-[10px] font-medium transition-colors"
      >
        Approve
      </button>
      <button
        onClick={() => handleAction('pause')}
        disabled={isRunning}
        className="bg-amber-500/20 text-amber-400 hover:bg-amber-500/30 px-2 py-0.5 rounded text-[10px] font-medium transition-colors"
      >
        Pause
      </button>
      <button
        onClick={() => handleAction('cancel')}
        disabled={isRunning}
        className="bg-red-500/20 text-red-400 hover:bg-red-500/30 px-2 py-0.5 rounded text-[10px] font-medium transition-colors"
      >
        Abort
      </button>
    </div>
  );
}
