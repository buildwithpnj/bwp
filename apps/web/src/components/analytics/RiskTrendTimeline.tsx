'use client';

export function RiskTrendTimeline() {
  return (
    <div className="bg-muted/30 border border-border p-3.5 rounded-xl space-y-2 text-xs">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold font-mono">Predicted Risk Trend Timeline</span>
      <div className="space-y-3 pl-2 border-l border-border/80 ml-1">
        <div className="relative">
          <div className="absolute -left-[13px] top-1.5 w-2 h-2 rounded-full bg-emerald-400" />
          <span className="font-semibold text-foreground text-[10px]">T-3 Hours: Low Stable baseline</span>
          <p className="text-[9px] text-muted-foreground">Stable operations across all active node targets.</p>
        </div>
        <div className="relative">
          <div className="absolute -left-[13px] top-1.5 w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
          <span className="font-semibold text-foreground text-[10px]">Next 2 Hours: Rising Latency Warning</span>
          <p className="text-[9px] text-muted-foreground">Moderate latency variance projected in downstream providers.</p>
        </div>
      </div>
    </div>
  );
}
export default RiskTrendTimeline;
