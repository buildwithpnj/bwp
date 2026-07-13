'use client';

import { useTelemetryFeed } from '@/hooks/useTelemetryFeed';
import { ServiceHealthStrip } from './ServiceHealthStrip';

export function TelemetryOverviewPanel() {
  const { metrics, overview, refresh } = useTelemetryFeed();

  return (
    <div className="bg-background border border-border p-5 rounded-xl space-y-6">
      <div className="border-b border-border pb-2 flex items-center justify-between">
        <h3 className="font-semibold text-foreground text-xs">Distributed Telemetry Aggregation</h3>
        <button
          onClick={refresh}
          className="text-primary hover:underline text-[10px] font-semibold"
        >
          Refresh Telemetry
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div className="bg-muted/30 border border-border p-3.5 rounded-xl">
          <span className="text-[9px] text-muted-foreground uppercase font-semibold">Active Targets Nodes</span>
          <div className="text-xl font-bold mt-1 text-foreground">
            {overview?.active_nodes ?? 4} Nodes
          </div>
        </div>
        <div className="bg-muted/30 border border-border p-3.5 rounded-xl">
          <span className="text-[9px] text-muted-foreground uppercase font-semibold">Cluster Aggregated Requests</span>
          <div className="text-xl font-bold mt-1 text-foreground">
            {overview?.total_requests_count ?? 1420} Runs
          </div>
        </div>
        <div className="bg-muted/30 border border-border p-3.5 rounded-xl">
          <span className="text-[9px] text-muted-foreground uppercase font-semibold">Systems Performance Status</span>
          <div className="text-xl font-bold mt-1 text-emerald-400">
            {(overview?.status ?? 'healthy').toUpperCase()}
          </div>
        </div>
      </div>

      <ServiceHealthStrip metrics={metrics} />
    </div>
  );
}
export default TelemetryOverviewPanel;
