import { useState, useEffect } from 'react';

export function useRetrievalEvals() {
  const [evalResults, setEvalResults] = useState<any>(null);
  const [running, setRunning] = useState(false);

  const fetchEvalStats = async () => {
    try {
      const res = await fetch('/api/retrieval/evals/metrics');
      if (res.ok) {
        const data = await res.json();
        setEvalResults(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const executeEvalRun = async (dataset: string) => {
    setRunning(true);
    try {
      const res = await fetch(`/api/retrieval/evals/run?dataset_name=${dataset}`, { method: 'POST' });
      if (res.ok) {
        await fetchEvalStats();
        return true;
      }
    } catch (e) {
      console.error(e);
    } finally {
      setRunning(false);
    }
    return false;
  };

  useEffect(() => {
    fetchEvalStats();
  }, []);

  return { evalResults, running, executeEvalRun, refresh: fetchEvalStats };
}
