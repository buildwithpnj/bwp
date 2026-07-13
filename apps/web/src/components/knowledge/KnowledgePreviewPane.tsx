'use client';

interface KnowledgePreviewPaneProps {
  documents: any[];
}

export function KnowledgePreviewPane({ documents }: KnowledgePreviewPaneProps) {
  const activeDoc = documents[0];
  return (
    <div className="space-y-2 text-xs">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Canonical Document Text Preview</span>
      <div className="border border-border/85 rounded-lg p-3 bg-background/50 h-[250px] overflow-y-auto">
        {activeDoc ? (
          <div className="space-y-2">
            <h4 className="font-bold text-foreground text-sm border-b border-border/40 pb-1">{activeDoc.title}</h4>
            <p className="text-[10px] text-muted-foreground leading-normal whitespace-pre-wrap">{activeDoc.canonical_text}</p>
          </div>
        ) : (
          <p className="text-muted-foreground text-[10px] text-center pt-16">No document selected to preview.</p>
        )}
      </div>
    </div>
  );
}
export default KnowledgePreviewPane;
