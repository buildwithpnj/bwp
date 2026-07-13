'use client';

import { useKnowledgeExplorer } from '@/hooks/useKnowledgeExplorer';
import { KnowledgeFileTree } from './KnowledgeFileTree';
import { KnowledgePreviewPane } from './KnowledgePreviewPane';
import { KnowledgeHealthPanel } from './KnowledgeHealthPanel';
import { IndexRunHistory } from './IndexRunHistory';
import { RetrievalTraceCard } from './RetrievalTraceCard';

export function KnowledgeExplorer() {
  const { documents, runs, refresh } = useKnowledgeExplorer();

  return (
    <div className="bg-background border border-border p-5 rounded-xl space-y-6">
      <div className="border-b border-border pb-2 flex items-center justify-between">
        <h3 className="font-semibold text-foreground text-xs">Knowledge Base & Ingestion Explorer</h3>
        <button
          onClick={refresh}
          className="text-primary hover:underline text-[10px] font-semibold"
        >
          Rescan Index
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1 border border-border/80 rounded-xl p-3 bg-muted/20">
          <KnowledgeFileTree documents={documents} />
        </div>
        <div className="md:col-span-2 border border-border/80 rounded-xl p-3 bg-muted/20">
          <KnowledgePreviewPane documents={documents} />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-border/40">
        <KnowledgeHealthPanel />
        <IndexRunHistory runs={runs} />
      </div>

      <div className="pt-4 border-t border-border/40">
        <RetrievalTraceCard />
      </div>
    </div>
  );
}
export default KnowledgeExplorer;
