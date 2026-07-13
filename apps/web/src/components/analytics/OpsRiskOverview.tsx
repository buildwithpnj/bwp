'use client';

import { useOpsRisk } from '@/hooks/useOpsRisk';
import { FailurePatternTable } from './FailurePatternTable';
import { PredictiveIncidentPanel } from './PredictiveIncidentPanel';
import { PreventionRecommendationCard } from './PreventionRecommendationCard';
import { RiskTrendTimeline } from './RiskTrendTimeline';

export function OpsRiskOverview() {
  const { riskOverview, patterns, predictions, recs, refresh } = useOpsRisk();

  return (
    <div className="bg-background border border-border p-5 rounded-xl space-y-6">
      <div className="border-b border-border pb-2 flex items-center justify-between">
        <h3 className="font-semibold text-foreground text-xs">Predictive failure & Risk Analytics</h3>
        <button
          onClick={refresh}
          className="text-primary hover:underline text-[10px] font-semibold"
        >
          Recalculate Predictions
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div className="bg-muted/30 border border-border p-3.5 rounded-xl">
          <span className="text-[9px] text-muted-foreground uppercase font-semibold">Active Risk Scope</span>
          <div className="text-xl font-bold mt-1 text-foreground">
            {riskOverview?.cluster_scope ?? 'production_cluster'}
          </div>
        </div>
        <div className="bg-muted/30 border border-border p-3.5 rounded-xl">
          <span className="text-[9px] text-muted-foreground uppercase font-semibold">Forecasting Confidence</span>
          <div className="text-xl font-bold mt-1 text-foreground">
            {((riskOverview?.confidence_score ?? 0.95) * 100).toFixed(0)}%
          </div>
        </div>
        <div className="bg-muted/30 border border-border p-3.5 rounded-xl">
          <span className="text-[9px] text-muted-foreground uppercase font-semibold">Current Risk Rating</span>
          <div className="text-xl font-bold mt-1 text-emerald-400">
            {riskOverview?.risk_score ? `${(riskOverview.risk_score * 100).toFixed(0)}%` : '12%'}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <PredictiveIncidentPanel predictions={predictions} />
        <PreventionRecommendationCard recs={recs} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-border/40">
        <FailurePatternTable patterns={patterns} />
        <RiskTrendTimeline />
      </div>
    </div>
  );
}
export default OpsRiskOverview;
