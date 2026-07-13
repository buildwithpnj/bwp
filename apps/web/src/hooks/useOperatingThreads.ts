import { useState, useEffect } from 'react';

export interface OperatingThread {
  id: string;
  title: string;
  description?: string;
  status: 'active' | 'paused' | 'archived';
  created_at: string;
}

export function useOperatingThreads() {
  const [threads, setThreads] = useState<OperatingThread[]>([]);
  const [activeThread, setActiveThread] = useState<OperatingThread | null>(null);

  const fetchThreads = async () => {
    try {
      const res = await fetch('/api/threads/list');
      if (res.ok) {
        const data = await res.json();
        setThreads(data);
        const active = data.find((t: OperatingThread) => t.status === 'active');
        setActiveThread(active || null);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchThreads();
  }, []);

  const createThread = async (title: string, description: string) => {
    try {
      const res = await fetch('/api/threads/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description })
      });
      if (res.ok) {
        const newThread = await res.json();
        // pause other threads
        if (activeThread) {
          await transitionThread(activeThread.id, 'paused');
        }
        setThreads(prev => [newThread, ...prev.map(t => t.status === 'active' ? { ...t, status: 'paused' as const } : t)]);
        setActiveThread(newThread);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const transitionThread = async (id: string, status: 'active' | 'paused' | 'archived') => {
    try {
      const res = await fetch(`/api/threads/${id}/transition?new_status=${status}`, { method: 'POST' });
      if (res.ok) {
        await fetchThreads();
      }
    } catch (e) {
      console.error(e);
    }
  };

  return {
    threads,
    activeThread,
    createThread,
    transitionThread,
    fetchThreads
  };
}
