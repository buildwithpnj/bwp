'use client';

interface ReleaseGatePanelProps {
  rolloutId: string;
  onApprove: () => void;
}

export function ReleaseGatePanel({ rolloutId, onApprove }: ReleaseGatePanelProps) {
  return (
    <div className="bg-muted/30 border border-border p-3.5 rounded-xl space-y-3">
      <h4 className="font-semibold text-foreground text-xs">Stage-Gate Release Approvals</h4>
      <p className="text-[10px] text-muted-foreground leading-normal">
        Requires administrator clearance before promoting rollout scopes to wider clusters.
      </p>
      <button
        onClick={onApprove}
        className="bg-primary text-primary-foreground hover:bg-primary/90 border border-border/40 px-3 py-1.5 rounded-md text-xs font-semibold w-full transition-all"
      >
        Sign Manual Approval Event
      </button>
    </div>
  );
}
export default ReleaseGatePanel;
