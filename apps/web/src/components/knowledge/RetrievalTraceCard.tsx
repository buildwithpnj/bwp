'use client';

import { useState } from 'react';
import { useRetrievalTrace } from '@/hooks/useRetrievalTrace';
import { EvidencePanel } from './EvidencePanel';
import { RetrievalFeedbackBar } from './RetrievalFeedbackBar';

import { GroundingWarningBadge } from './GroundingWarningBadge';

export function RetrievalTraceCard() {
  const [query, setQuery] = useState('');
  const { result, loading, queryRAG, submitFeedback } = useRetrievalTrace();

  const handleQuery = async () => {
    if (!query.trim()) return;
    await queryRAG(query, 'tenant_123', 'governance');
  };

  return (
    <div className="bg-muted/10 border border-border p-4 rounded-xl space-y-4 text-xs">
      <span className="text-[9px] text-muted-foreground uppercase font-semibold">Grounded RAG Trace Tracer</span>
      <div className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask policy index (e.g. sync configuration)..."
          className="bg-background border border-border px-3 py-1.5 rounded-lg flex-1 text-xs text-foreground focus:outline-none focus:border-primary/50"
        />
        <button
          onClick={handleQuery}
          disabled={loading}
          className="bg-primary text-primary-foreground hover:bg-primary/95 px-4 py-1.5 rounded-lg font-semibold"
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {result && (
        <div className="space-y-4 pt-2 border-t border-border/40">
          <div className="flex justify-between items-center bg-muted/30 p-2.5 rounded-lg">
            <div>
              <span className="text-muted-foreground text-[10px]">Rewritten query expansion:</span>
              <p className="font-semibold text-foreground mt-0.5">{result.query_text}</p>
            </div>
            <div className="text-right flex items-center gap-2">
              <div>
                <span className="text-muted-foreground text-[10px]">Confidence:</span>
                <p className="font-bold text-emerald-400 mt-0.5">{((result.confidence_score ?? 0) * 100).toFixed(0)}%</p>
              </div>
              <GroundingWarningBadge score={result.confidence_score} />
            </div>
          </div>

          <EvidencePanel chunks={result.chunks} />

          <RetrievalFeedbackBar
            traceId={result.trace_id}
            onSubmitFeedback={submitFeedback}
          />
        </div>
      )}
    </div>
  );
}
export default RetrievalTraceCard;
