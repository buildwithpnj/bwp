'use client';

interface PolicyDiffPreviewProps {
  diff: Record<string, { old: string; new: string }> | null;
}

export function PolicyDiffPreview({ diff }: PolicyDiffPreviewProps) {
  if (!diff) return null;
  return (
    <div className="bg-muted/40 border border-border p-3.5 rounded-xl space-y-2 text-xs">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Divergence Comparison Preview</span>
      <div className="space-y-2">
        {Object.entries(diff).map(([key, val]) => (
          <div key={key} className="flex justify-between items-center border-b border-border/40 pb-1.5 last:border-0 last:pb-0">
            <span className="font-semibold text-foreground">{key}</span>
            <div className="flex gap-2">
              <span className="text-red-400 line-through">{val.old}</span>
              <span className="text-muted-foreground">→</span>
              <span className="text-emerald-400 font-medium">{val.new}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
export default PolicyDiffPreview;
