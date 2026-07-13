'use client';

interface RecoveryTimelineProps {
  history: any[];
}

export function RecoveryTimeline({ history }: RecoveryTimelineProps) {
  return (
    <div className="space-y-2">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Resilience History Trails</span>
      <div className="border border-border/80 rounded-lg overflow-hidden text-xs">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-muted/40 border-b border-border text-muted-foreground text-[10px]">
              <th className="p-2">Trigger Date</th>
              <th className="p-2">Affected Scope</th>
              <th className="p-2">Activated Modes Features</th>
            </tr>
          </thead>
          <tbody>
            {history.length === 0 ? (
              <tr>
                <td colSpan={3} className="p-3 text-center text-muted-foreground">
                  No previous degraded activations logs.
                </td>
              </tr>
            ) : (
              history.map((h, idx) => (
                <tr key={idx} className="border-b border-border/50 hover:bg-muted/10 last:border-0">
                  <td className="p-2 text-muted-foreground">{h.created_at ?? 'just now'}</td>
                  <td className="p-2 text-foreground font-semibold">{h.affected_scope}</td>
                  <td className="p-2 text-primary font-medium">{h.activated_features}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
export default RecoveryTimeline;
