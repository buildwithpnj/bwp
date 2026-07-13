'use client';

import { NotificationEvent } from '@/hooks/useNotificationFeed';
import { NotificationActionBar } from './NotificationActionBar';
import { cn } from '@/lib/utils';

interface NotificationItemProps {
  item: NotificationEvent;
  onDismiss: (id: string) => void;
}

export function NotificationItem({ item, onDismiss }: NotificationItemProps) {
  return (
    <div
      className={cn(
        'p-3 rounded-lg border text-left transition-all duration-200',
        item.priority === 'high'
          ? 'bg-red-500/5 border-red-500/20'
          : 'bg-muted/30 border-border',
        item.status === 'read' && 'opacity-60'
      )}
    >
      <div className="flex items-start justify-between">
        <div>
          <h4 className="font-semibold text-foreground text-xs">{item.title}</h4>
          {item.description && (
            <p className="text-[10px] text-muted-foreground mt-0.5 leading-normal">
              {item.description}
            </p>
          )}
        </div>
        <button
          onClick={() => onDismiss(item.id)}
          className="text-muted-foreground hover:text-foreground text-[10px] p-0.5 hover:bg-muted rounded"
        >
          Dismiss
        </button>
      </div>

      <NotificationActionBar
        notificationId={item.id}
        sourceType={item.source_type}
        onActionComplete={() => onDismiss(item.id)}
      />
    </div>
  );
}
