'use client';

import { useState } from 'react';
import { useNotificationFeed } from '@/hooks/useNotificationFeed';
import { NotificationBadge } from './NotificationBadge';
import { NotificationItem } from './NotificationItem';

export function NotificationCenter() {
  const [isOpen, setIsOpen] = useState(false);
  const { notifications, unreadCount, dismissNotification } = useNotificationFeed();

  const filtered = notifications.filter(n => n.status !== 'dismissed');

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-1.5 rounded-md hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          className="w-5 h-5"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0"
          />
        </svg>
        <NotificationBadge count={unreadCount} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 z-50 w-72 bg-background/95 border border-border shadow-2xl rounded-lg p-3 backdrop-blur-md flex flex-col gap-3">
          <div className="flex items-center justify-between border-b border-border/50 pb-2">
            <h3 className="font-semibold text-foreground text-xs">Active Alerts</h3>
            <span className="text-[10px] text-muted-foreground">{unreadCount} pending</span>
          </div>

          <div className="flex-1 overflow-y-auto max-h-60 space-y-2.5">
            {filtered.length === 0 ? (
              <p className="text-[10px] text-muted-foreground text-center py-4">
                No active intervention alerts.
              </p>
            ) : (
              filtered.map(item => (
                <NotificationItem
                  key={item.id}
                  item={item}
                  onDismiss={dismissNotification}
                />
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
export default NotificationCenter;
