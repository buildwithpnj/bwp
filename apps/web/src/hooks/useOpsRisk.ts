import { useState, useEffect } from 'react';

export function useOpsRisk() {
  const [riskOverview, setRiskOverview] = useState<any>(null);
  const [patterns, setPatterns] = useState<any[]>([]);
  const [predictions, setPredictions] = useState<any[]>([]);
  const [recs, setRecs] = useState<any[]>([]);

  const fetchRisk = async () => {
    try {
      const res = await fetch('/api/ops/risk/overview');
      if (res.ok) {
        const data = await res.json();
        setRiskOverview(data);
      }
      
      const patternsRes = await fetch('/api/ops/risk/patterns');
      if (patternsRes.ok) {
        const patternsData = await patternsRes.json();
        setPatterns(patternsData);
      }
      
      const predictionsRes = await fetch('/api/ops/risk/predictions');
      if (predictionsRes.ok) {
        const predictionsData = await predictionsRes.json();
        setPredictions(predictionsData);
      }
      
      const recsRes = await fetch('/api/ops/risk/recommendations');
      if (recsRes.ok) {
        const recsData = await recsRes.json();
        setRecs(recsData);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchRisk();
  }, []);

  return { riskOverview, patterns, predictions, recs, refresh: fetchRisk };
}
