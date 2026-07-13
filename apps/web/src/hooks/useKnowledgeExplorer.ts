import { useState, useEffect } from 'react';

export function useKnowledgeExplorer() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [runs, setRuns] = useState<any[]>([]);

  const fetchKnowledge = async () => {
    try {
      const res = await fetch('/api/knowledge/documents');
      if (res.ok) {
        const data = await res.json();
        setDocuments(data);
      }
      
      const runsRes = await fetch('/api/knowledge/index/history');
      if (runsRes.ok) {
        const runsData = await runsRes.json();
        setRuns(runsData);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchKnowledge();
  }, []);

  return { documents, runs, refresh: fetchKnowledge };
}
