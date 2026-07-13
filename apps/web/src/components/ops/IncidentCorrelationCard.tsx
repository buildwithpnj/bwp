'use client';

export function IncidentCorrelationCard() {
  return (
    <div className="bg-muted/30 border border-border p-3.5 rounded-xl space-y-2 text-xs">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold font-mono">Incident Correlation Link Map</span>
      <div className="flex gap-4 items-center pl-2">
        <div className="flex flex-col border border-border/80 p-2 rounded bg-background/50">
          <span className="font-semibold text-foreground text-[10px]">CPU Utilization Peak</span>
          <span className="text-[8px] text-muted-foreground">ID: cpu_util</span>
        </div>
        <span className="text-muted-foreground font-semibold">→</span>
        <div className="flex flex-col border border-border/80 p-2 rounded bg-background/50">
          <span className="font-semibold text-foreground text-[10px]">Model Latency Spike</span>
          <span className="text-[8px] text-muted-foreground">ID: latency_spike</span>
        </div>
      </div>
    </div>
  );
}
export default IncidentCorrelationCard;
