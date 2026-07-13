import { useState, useEffect } from 'react';

export function useTelemetryFeed() {
  const [metrics, setMetrics] = useState<any[]>([]);
  const [overview, setOverview] = useState<any>(null);

  const fetchTelemetry = async () => {
    try {
      const res = await fetch('/api/telemetry/overview');
      if (res.ok) {
        const data = await res.json();
        setOverview(data);
      }
      
      const metricsRes = await fetch('/api/telemetry/metrics');
      if (metricsRes.ok) {
        const metricsData = await metricsRes.json();
        setMetrics(metricsData);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchTelemetry();
  }, []);

  return { metrics, overview, refresh: fetchTelemetry };
}
