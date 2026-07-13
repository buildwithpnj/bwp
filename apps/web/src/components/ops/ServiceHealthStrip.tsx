'use client';

import { MetricDriftBadge } from './MetricDriftBadge';

interface ServiceHealthStripProps {
  metrics: Array<{ metric_name: string; metric_value: number }>;
}

export function ServiceHealthStrip({ metrics }: ServiceHealthStripProps) {
  return (
    <div className="space-y-2">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Active Metrics Health Summary</span>
      <div className="border border-border/80 rounded-lg overflow-hidden text-xs">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-muted/40 border-b border-border text-muted-foreground text-[10px]">
              <th className="p-2">Metric Name</th>
              <th className="p-2">Value</th>
              <th className="p-2">Drift Indicators</th>
            </tr>
          </thead>
          <tbody>
            {metrics.length === 0 ? (
              <tr>
                <td colSpan={3} className="p-3 text-center text-muted-foreground">
                  No active metrics.
                </td>
              </tr>
            ) : (
              metrics.map((m, idx) => (
                <tr key={idx} className="border-b border-border/50 hover:bg-muted/10 last:border-0">
                  <td className="p-2 font-mono text-foreground">{m.metric_name}</td>
                  <td className="p-2 font-semibold text-foreground">{m.metric_value}%</td>
                  <td className="p-2">
                    <MetricDriftBadge value={m.metric_value} />
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
export default ServiceHealthStrip;
