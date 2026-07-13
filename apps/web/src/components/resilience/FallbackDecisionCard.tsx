'use client';

export function FallbackDecisionCard() {
  return (
    <div className="bg-muted/30 border border-border p-3.5 rounded-xl space-y-2 text-xs">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Active Fallback Routing Paths</span>
      <div className="space-y-1.5 font-mono text-[10px]">
        <div className="flex justify-between border-b border-border/40 pb-1">
          <span className="text-muted-foreground">GPT-4o (Chat/Voice)</span>
          <span className="text-emerald-400 font-semibold">→ GPT-4o-Mini (Active)</span>
        </div>
        <div className="flex justify-between border-b border-border/40 pb-1">
          <span className="text-muted-foreground">Parallel Specialists</span>
          <span className="text-amber-400 font-semibold">→ Single Thread Queue</span>
        </div>
        <div className="flex justify-between">
          <span className="text-muted-foreground">Image/Multimodal</span>
          <span className="text-rose-400 font-semibold">→ Delayed Offline Cache</span>
        </div>
      </div>
    </div>
  );
}
export default FallbackDecisionCard;
