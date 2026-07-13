'use client';

interface IndexRunHistoryProps {
  runs: any[];
}

export function IndexRunHistory({ runs }: IndexRunHistoryProps) {
  return (
    <div className="bg-background/25 border border-border p-4 rounded-xl space-y-3 text-xs">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Indexing History Logs</span>
      <div className="border border-border/80 rounded-lg overflow-hidden max-h-[140px] overflow-y-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-muted/40 border-b border-border text-muted-foreground text-[10px]">
              <th className="p-2">Trigger Date</th>
              <th className="p-2">Status</th>
              <th className="p-2">Documents Added</th>
            </tr>
          </thead>
          <tbody>
            {runs.length === 0 ? (
              <tr>
                <td colSpan={3} className="p-2 text-center text-muted-foreground">
                  No index run executions logged.
                </td>
              </tr>
            ) : (
              runs.map((r, idx) => (
                <tr key={idx} className="border-b border-border/50 hover:bg-muted/10 last:border-0">
                  <td className="p-2 text-muted-foreground">{r.created_at ?? 'just now'}</td>
                  <td className="p-2 font-semibold text-emerald-400 capitalize">{r.status}</td>
                  <td className="p-2 text-foreground font-mono">{r.documents_added}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
export default IndexRunHistory;
