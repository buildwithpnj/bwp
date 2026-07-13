import { useState } from 'react';

export interface SyncJob {
  id: string;
  source_env: string;
  target_env: string;
  status: string;
  created_at: string;
}

export function usePolicySync() {
  const [jobs, setJobs] = useState<SyncJob[]>([]);
  const [diff, setDiff] = useState<any>(null);
  const [isSyncing, setIsSyncing] = useState(false);

  const previewSync = async (source: string, target: string) => {
    try {
      const res = await fetch(`/api/governance/sync/preview?source_env=${source}&target_env=${target}`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setDiff(data.diff);
        return data;
      }
    } catch (e) {
      console.error(e);
    }
    return null;
  };

  const applySync = async (source: string, target: string, signature: string) => {
    setIsSyncing(true);
    try {
      const res = await fetch('/api/governance/sync/apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          source_env: source,
          target_env: target,
          target_nodes: ['10.0.0.1'],
          target_tenants: ['tenant_1'],
          signature
        })
      });
      if (res.ok) {
        const job = await res.json();
        setJobs(prev => [job, ...prev]);
        setDiff(null);
        return true;
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsSyncing(false);
    }
    return false;
  };

  const triggerRollback = async (jobId: string) => {
    try {
      const res = await fetch(`/api/governance/sync/rollback/apply?job_id=${jobId}`, { method: 'POST' });
      return res.ok;
    } catch (e) {
      console.error(e);
      return false;
    }
  };

  return {
    jobs,
    diff,
    isSyncing,
    previewSync,
    applySync,
    triggerRollback
  };
}
