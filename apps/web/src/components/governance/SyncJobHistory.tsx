'use client';

import { SyncJob } from '@/hooks/usePolicySync';

interface SyncJobHistoryProps {
  jobs: SyncJob[];
  onRollback: (jobId: string) => void;
}

export function SyncJobHistory({ jobs, onRollback }: SyncJobHistoryProps) {
  return (
    <div className="space-y-2">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Federated Sync Jobs</span>
      <div className="border border-border rounded-lg overflow-hidden text-xs">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-muted/40 border-b border-border text-muted-foreground text-[10px]">
              <th className="p-2">Job ID</th>
              <th className="p-2">Source</th>
              <th className="p-2">Target</th>
              <th className="p-2">Status</th>
              <th className="p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {jobs.length === 0 ? (
              <tr>
                <td colSpan={5} className="p-4 text-center text-muted-foreground">
                  No sync executions logs.
                </td>
              </tr>
            ) : (
              jobs.map(job => (
                <tr key={job.id} className="border-b border-border/50 hover:bg-muted/10 last:border-0">
                  <td className="p-2 font-mono text-[10px] text-foreground truncate max-w-[80px]">{job.id}</td>
                  <td className="p-2 text-muted-foreground">{job.source_env}</td>
                  <td className="p-2 text-muted-foreground">{job.target_env}</td>
                  <td className="p-2 text-primary font-medium">{job.status}</td>
                  <td className="p-2">
                    <button
                      onClick={() => onRollback(job.id)}
                      className="text-red-400 hover:text-red-300 underline font-semibold text-[10px]"
                    >
                      Rollback
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
export default SyncJobHistory;
