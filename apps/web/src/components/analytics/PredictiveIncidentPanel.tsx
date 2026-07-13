'use client';

interface PredictiveIncidentPanelProps {
  predictions: any[];
}

export function PredictiveIncidentPanel({ predictions }: PredictiveIncidentPanelProps) {
  return (
    <div className="space-y-2 text-xs">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Predictive Warnings Signals</span>
      <div className="border border-border/80 rounded-lg p-3.5 space-y-3 bg-muted/20">
        {predictions.length === 0 ? (
          <p className="text-[10px] text-muted-foreground leading-normal">
            No predictive regressions signals detected on nodes.
          </p>
        ) : (
          predictions.map((p, idx) => (
            <div key={idx} className="border-b border-border/40 pb-2 last:border-0 last:pb-0">
              <h5 className="font-semibold text-foreground">{p.pattern_family}</h5>
              <p className="text-[9px] text-muted-foreground">{p.leading_signals}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
export default PredictiveIncidentPanel;
