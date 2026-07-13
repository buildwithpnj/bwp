import { useState } from 'react';

export function useRetrievalTrace() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const queryRAG = async (query: string, tenantId: string, pageScope?: string) => {
    setLoading(true);
    try {
      const res = await fetch('/api/retrieval/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, tenant_id: tenantId, page_scope: pageScope })
      });
      if (res.ok) {
        const data = await res.json();
        setResult(data);
        return data;
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
    return null;
  };

  const submitFeedback = async (traceId: string, score: number, notes: string) => {
    try {
      const res = await fetch(`/api/retrieval/feedback?trace_id=${traceId}&score=${score}&notes=${notes}`, {
        method: 'POST'
      });
      return res.ok;
    } catch (e) {
      console.error(e);
    }
    return false;
  };

  return { result, loading, queryRAG, submitFeedback };
}
