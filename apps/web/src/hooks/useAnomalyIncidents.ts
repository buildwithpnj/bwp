import { useState, useEffect } from 'react';

export function useAnomalyIncidents() {
  const [incidents, setIncidents] = useState<any[]>([]);

  const fetchIncidents = async () => {
    try {
      const res = await fetch('/api/anomalies/incidents');
      if (res.ok) {
        const data = await res.json();
        setIncidents(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const acknowledgeIncident = async (id: string) => {
    try {
      const res = await fetch(`/api/anomalies/incidents/${id}/acknowledge`, { method: 'POST' });
      if (res.ok) {
        fetchIncidents();
        return true;
      }
    } catch (e) {
      console.error(e);
    }
    return false;
  };

  const resolveIncident = async (id: string) => {
    try {
      const res = await fetch(`/api/anomalies/incidents/${id}/resolve`, { method: 'POST' });
      if (res.ok) {
        fetchIncidents();
        return true;
      }
    } catch (e) {
      console.error(e);
    }
    return false;
  };

  useEffect(() => {
    fetchIncidents();
  }, []);

  return { incidents, acknowledgeIncident, resolveIncident, refresh: fetchIncidents };
}
