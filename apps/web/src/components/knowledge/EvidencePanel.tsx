'use client';

interface EvidencePanelProps {
  chunks: any[];
}

export function EvidencePanel({ chunks }: EvidencePanelProps) {
  return (
    <div className="space-y-2 text-xs">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Matched Source Chunks & Grounding citations</span>
      <div className="space-y-2.5 max-h-[220px] overflow-y-auto">
        {chunks.length === 0 ? (
          <p className="text-muted-foreground text-[10px] text-center py-4 bg-muted/10 rounded-lg">
            No grounding source chunks matched this query.
          </p>
        ) : (
          chunks.map((c, idx) => (
            <div key={idx} className="bg-background border border-border/80 p-3 rounded-xl space-y-1.5">
              <div className="flex justify-between items-center text-[9px] font-mono border-b border-border/30 pb-1">
                <span className="text-muted-foreground">Chunk {c.chunk_id.substring(0, 8)}</span>
                <span className="text-emerald-400 font-bold">{(c.confidence_score * 100).toFixed(0)}% Relevance</span>
              </div>
              <p className="text-[10px] text-foreground font-mono bg-muted/30 p-2 rounded border border-border/40 whitespace-pre-wrap leading-normal">
                {c.chunk_text}
              </p>
              <div className="flex items-center gap-1.5 text-[8px] text-muted-foreground">
                <span className="bg-primary/20 text-primary px-1.5 py-0.5 rounded font-semibold uppercase">Source summary:</span>
                <span>{c.chunk_summary}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
export default EvidencePanel;
