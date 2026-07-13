'use client';

import { useState } from 'react';
import { usePolicySync } from '@/hooks/usePolicySync';
import { PolicyDiffPreview } from './PolicyDiffPreview';
import { SyncJobHistory } from './SyncJobHistory';
import { FederatedRollbackPanel } from './FederatedRollbackPanel';

export function PolicySyncPanel() {
  const { jobs, diff, isSyncing, previewSync, applySync, triggerRollback } = usePolicySync();
  const [source, setSource] = useState('staging');
  const [target, setTarget] = useState('production');
  const [sig, setSig] = useState('sig_admin_key_1234');

  const handlePreview = async () => {
    await previewSync(source, target);
  };

  const handleApply = async () => {
    await applySync(source, target, sig);
  };

  return (
    <div className="bg-background border border-border p-5 rounded-xl space-y-6">
      <div className="border-b border-border pb-2 flex items-center justify-between">
        <h3 className="font-semibold text-foreground text-xs">Federated Governance Policy Sync</h3>
        <span className="text-[10px] text-muted-foreground">Cluster Sync Engine</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="flex flex-col gap-1.5 text-xs">
          <label className="text-muted-foreground font-medium">Source Environment</label>
          <input
            type="text"
            value={source}
            onChange={e => setSource(e.target.value)}
            className="bg-muted border border-border px-3 py-1.5 rounded-md text-foreground"
          />
        </div>
        <div className="flex flex-col gap-1.5 text-xs">
          <label className="text-muted-foreground font-medium">Target Environment</label>
          <input
            type="text"
            value={target}
            onChange={e => setTarget(e.target.value)}
            className="bg-muted border border-border px-3 py-1.5 rounded-md text-foreground"
          />
        </div>
        <div className="flex flex-col gap-1.5 text-xs">
          <label className="text-muted-foreground font-medium">Crypto Signature</label>
          <input
            type="text"
            value={sig}
            onChange={e => setSig(e.target.value)}
            className="bg-muted border border-border px-3 py-1.5 rounded-md text-foreground"
          />
        </div>
      </div>

      <div className="flex gap-3">
        <button
          onClick={handlePreview}
          className="bg-muted hover:bg-accent border border-border text-foreground px-4 py-1.5 rounded-md text-xs font-semibold"
        >
          Preview Divergence Diff
        </button>
        <button
          onClick={handleApply}
          disabled={isSyncing}
          className="bg-primary text-primary-foreground hover:bg-primary/95 disabled:opacity-50 px-4 py-1.5 rounded-md text-xs font-semibold"
        >
          {isSyncing ? 'Syncing...' : 'Apply Signed Sync'}
        </button>
      </div>

      <PolicyDiffPreview diff={diff} />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-border/40">
        <SyncJobHistory jobs={jobs} onRollback={triggerRollback} />
        <FederatedRollbackPanel onRollback={triggerRollback} />
      </div>
    </div>
  );
}
export default PolicySyncPanel;
