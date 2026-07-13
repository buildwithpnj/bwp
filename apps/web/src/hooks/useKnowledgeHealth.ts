import { useState, useEffect } from 'react';

export function useKnowledgeHealth() {
  const [report, setReport] = useState<any>(null);
  const [evals, setEvals] = useState<any>(null);

  const fetchHealth = async () => {
    try {
      const res = await fetch('/api/knowledge/health');
      if (res.ok) {
        const data = await res.json();
        setReport(data);
      }
      
      const evalsRes = await fetch('/api/retrieval/evals/metrics');
      if (evalsRes.ok) {
        const evalsData = await evalsRes.json();
        setEvals(evalsData);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  return { report, evals, refresh: fetchHealth };
}
