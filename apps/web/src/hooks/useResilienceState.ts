import { useState, useEffect } from 'react';

export function useResilienceState() {
  const [resilienceState, setResilienceState] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);

  const fetchState = async () => {
    try {
      const res = await fetch('/api/resilience/state');
      if (res.ok) {
        const data = await res.json();
        setResilienceState(data);
      }
      
      const historyRes = await fetch('/api/resilience/history');
      if (historyRes.ok) {
        const historyData = await historyRes.json();
        setHistory(historyData);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const manuallyActivateDegraded = async (scope: string, activeFeatures: string, disabledFeatures: string) => {
    try {
      const res = await fetch(`/api/resilience/degraded/activate?scope=${scope}&active_features=${activeFeatures}&disabled_features=${disabledFeatures}`, { method: 'POST' });
      if (res.ok) {
        fetchState();
        return true;
      }
    } catch (e) {
      console.error(e);
    }
    return false;
  };

  const manualOverride = async () => {
    try {
      const res = await fetch('/api/resilience/degraded/override', { method: 'POST' });
      if (res.ok) {
        fetchState();
        return true;
      }
    } catch (e) {
      console.error(e);
    }
    return false;
  };

  useEffect(() => {
    fetchState();
  }, []);

  return { resilienceState, history, manuallyActivateDegraded, manualOverride, refresh: fetchState };
}
