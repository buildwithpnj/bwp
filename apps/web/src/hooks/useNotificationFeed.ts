import { useState, useEffect } from 'react';

export interface NotificationEvent {
  id: string;
  source_type: string;
  title: string;
  description?: string;
  priority: 'high' | 'medium' | 'low';
  status: 'unread' | 'read' | 'dismissed';
  created_at: string;
}

export function useNotificationFeed() {
  const [notifications, setNotifications] = useState<NotificationEvent[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);

  const fetchFeed = async () => {
    try {
      const res = await fetch('/api/notifications/feed');
      if (res.ok) {
        const data = await res.json();
        setNotifications(data);
        setUnreadCount(data.filter((n: NotificationEvent) => n.status === 'unread').length);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchFeed();
    const interval = setInterval(fetchFeed, 10000);
    return () => clearInterval(interval);
  }, []);

  const dismissNotification = async (id: string) => {
    try {
      const res = await fetch(`/api/notifications/${id}/dismiss`, { method: 'POST' });
      if (res.ok) {
        setNotifications(prev => prev.map(n => n.id === id ? { ...n, status: 'dismissed' } : n));
        setUnreadCount(prev => Math.max(prev - 1, 0));
      }
    } catch (e) {
      console.error(e);
    }
  };

  return {
    notifications,
    unreadCount,
    fetchFeed,
    dismissNotification
  };
}
