'use client';

import { useAnomalyIncidents } from '@/hooks/useAnomalyIncidents';
import { IncidentCorrelationCard } from './IncidentCorrelationCard';

export function AnomalyIncidentFeed() {
  const { incidents, acknowledgeIncident, resolveIncident, refresh } = useAnomalyIncidents();

  return (
    <div className="bg-background border border-border p-5 rounded-xl space-y-6">
      <div className="border-b border-border pb-2 flex items-center justify-between">
        <h3 className="font-semibold text-foreground text-xs">Active Anomaly Incidents</h3>
        <button
          onClick={refresh}
          className="text-primary hover:underline text-[10px] font-semibold"
        >
          Refresh Incidents
        </button>
      </div>

      <div className="space-y-4">
        {incidents.length === 0 ? (
          <p className="text-xs text-muted-foreground text-center py-4">No active anomalies detected.</p>
        ) : (
          incidents.map(inc => (
            <div key={inc.id} className="bg-muted/20 border border-border/80 p-3.5 rounded-xl space-y-3 text-xs flex justify-between items-start">
              <div className="space-y-1 max-w-[70%]">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-[9px] uppercase tracking-wider text-muted-foreground">ID: {inc.id.substring(0, 8)}</span>
                  <span className="text-[9px] bg-rose-500/20 text-rose-400 border border-rose-500/10 px-2 py-0.5 rounded-full font-semibold capitalize">{inc.severity}</span>
                </div>
                <h4 className="font-semibold text-foreground">{inc.signal_type}</h4>
                <p className="text-[10px] text-muted-foreground leading-normal">{inc.summary}</p>
              </div>

              <div className="flex gap-2">
                {inc.incident_status === 'active' && (
                  <button
                    onClick={() => acknowledgeIncident(inc.id)}
                    className="bg-muted hover:bg-accent border border-border px-2.5 py-1 rounded text-[10px] font-semibold text-foreground"
                  >
                    Acknowledge
                  </button>
                )}
                {inc.incident_status !== 'resolved' && (
                  <button
                    onClick={() => resolveIncident(inc.id)}
                    className="bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 border border-emerald-500/20 px-2.5 py-1 rounded text-[10px] font-semibold"
                  >
                    Resolve
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      <IncidentCorrelationCard />
    </div>
  );
}
export default AnomalyIncidentFeed;
