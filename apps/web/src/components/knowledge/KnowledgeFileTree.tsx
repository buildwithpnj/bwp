'use client';

interface KnowledgeFileTreeProps {
  documents: any[];
}

export function KnowledgeFileTree({ documents }: KnowledgeFileTreeProps) {
  return (
    <div className="space-y-2 text-xs">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Indexed Knowledge Source Files</span>
      <div className="space-y-1.5 max-h-[250px] overflow-y-auto">
        {documents.length === 0 ? (
          <p className="text-muted-foreground text-[10px]">No document sources indexed.</p>
        ) : (
          documents.map((doc, idx) => (
            <div key={idx} className="flex justify-between items-center p-2 rounded hover:bg-muted/30 cursor-pointer">
              <span className="font-mono text-[10px] text-foreground truncate max-w-[70%]">{doc.title}</span>
              <span className="text-[8px] bg-primary/20 text-primary border border-primary/15 px-2 py-0.5 rounded font-mono uppercase">{doc.source_type}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
export default KnowledgeFileTree;
