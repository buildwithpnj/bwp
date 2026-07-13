'use client';

interface RolloutHealthCardProps {
  healthScore: number;
  summary: string;
}

export function RolloutHealthCard({ healthScore, summary }: RolloutHealthCardProps) {
  const isHealthy = healthScore >= 0.8;
  return (
    <div className="bg-muted/30 border border-border p-3.5 rounded-xl flex flex-col justify-between text-xs">
      <div>
        <span className="text-[9px] text-muted-foreground uppercase font-semibold">Active Telemetry Health Score</span>
        <div className="flex items-baseline gap-2 mt-1">
          <span className={`text-2xl font-bold ${isHealthy ? 'text-emerald-400' : 'text-red-400'}`}>
            {(healthScore * 100).toFixed(0)}%
          </span>
          <span className="text-[10px] text-muted-foreground">Threshold: 80%</span>
        </div>
      </div>
      <div className="mt-3 text-[10px] text-muted-foreground leading-normal border-t border-border/40 pt-2.5">
        <span className="font-semibold text-foreground">Status Summary:</span> {summary}
      </div>
    </div>
  );
}
export default RolloutHealthCard;
