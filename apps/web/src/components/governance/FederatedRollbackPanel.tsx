'use client';

interface FederatedRollbackPanelProps {
  onRollback: (jobId: string) => void;
}

export function FederatedRollbackPanel({ onRollback }: FederatedRollbackPanelProps) {
  return (
    <div className="bg-muted/30 border border-border p-3.5 rounded-xl space-y-3">
      <h4 className="font-semibold text-foreground text-xs">Federated Rollback Preparedness</h4>
      <p className="text-[10px] text-muted-foreground leading-normal">
        Reverses configuration changes safely by mapping matching database backup snapshots.
      </p>
      <button
        onClick={() => onRollback('roll_backup_123')}
        className="bg-red-500/20 text-red-400 hover:bg-red-500/30 border border-red-500/30 px-3 py-1.5 rounded-md text-xs font-semibold w-full transition-all"
      >
        Revert Last Sync Changes
      </button>
    </div>
  );
}
export default FederatedRollbackPanel;
