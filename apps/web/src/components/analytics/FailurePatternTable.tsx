'use client';

interface FailurePatternTableProps {
  patterns: any[];
}

export function FailurePatternTable({ patterns }: FailurePatternTableProps) {
  return (
    <div className="space-y-2 text-xs">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Divergent Regressions Log</span>
      <div className="border border-border/80 rounded-lg overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-muted/40 border-b border-border text-muted-foreground text-[10px]">
              <th className="p-2">Pattern Name</th>
              <th className="p-2">Severity Rating</th>
            </tr>
          </thead>
          <tbody>
            {patterns.length === 0 ? (
              <tr>
                <td colSpan={2} className="p-3 text-center text-muted-foreground">
                  No active regressions recorded.
                </td>
              </tr>
            ) : (
              patterns.map((p, idx) => (
                <tr key={idx} className="border-b border-border/50 hover:bg-muted/10 last:border-0">
                  <td className="p-2 font-mono text-foreground">{p.pattern_family}</td>
                  <td className="p-2 text-rose-400 font-semibold">{((p.regression_score ?? 0) * 100).toFixed(0)}%</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
export default FailurePatternTable;
