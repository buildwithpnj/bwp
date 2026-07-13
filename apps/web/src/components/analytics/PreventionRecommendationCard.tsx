'use client';

interface PreventionRecommendationCardProps {
  recs: any[];
}

export function PreventionRecommendationCard({ recs }: PreventionRecommendationCardProps) {
  return (
    <div className="space-y-2 text-xs">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Proactive Prevention Recommendations</span>
      <div className="border border-border/80 rounded-lg p-3.5 space-y-3 bg-muted/20">
        {recs.length === 0 ? (
          <p className="text-[10px] text-muted-foreground leading-normal">
            No preventive recommendations suggested.
          </p>
        ) : (
          recs.map((r, idx) => (
            <div key={idx} className="flex justify-between items-center border-b border-border/40 pb-2 last:border-0 last:pb-0">
              <span className="font-semibold text-foreground truncate max-w-[70%]">{r.action}</span>
              <span className="text-[9px] bg-emerald-500/20 text-emerald-400 border border-emerald-500/10 px-2 py-0.5 rounded-full font-semibold capitalize">{r.risk_level}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
export default PreventionRecommendationCard;
