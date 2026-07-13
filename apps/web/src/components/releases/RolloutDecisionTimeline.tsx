'use client';

interface RolloutDecisionTimelineProps {
  percentage: number;
  status: string;
}

export function RolloutDecisionTimeline({ percentage, status }: RolloutDecisionTimelineProps) {
  return (
    <div className="bg-muted/30 border border-border p-3.5 rounded-xl space-y-2 text-xs">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold font-mono">Rollout Decision Timeline</span>
      <div className="space-y-3 pl-2 border-l border-border/80 ml-1">
        <div className="relative">
          <div className="absolute -left-[13px] top-1.5 w-2 h-2 rounded-full bg-emerald-400" />
          <span className="font-semibold text-foreground text-[10px]">Canary Rollout Initiated</span>
          <p className="text-[9px] text-muted-foreground">Assigned to initial 10% target targets.</p>
        </div>
        <div className="relative">
          <div className="absolute -left-[13px] top-1.5 w-2 h-2 rounded-full bg-primary" />
          <span className="font-semibold text-foreground text-[10px]">Promotion to {percentage}%</span>
          <p className="text-[9px] text-muted-foreground">Currently in status: <span className="font-mono text-foreground">{status}</span></p>
        </div>
      </div>
    </div>
  );
}
export default RolloutDecisionTimeline;
