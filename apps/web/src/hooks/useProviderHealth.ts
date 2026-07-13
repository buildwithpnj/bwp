import { useState, useEffect, useCallback } from 'react';

export interface ProviderHealth {
  status: 'healthy' | 'degraded' | 'offline';
  provider: string;
  base_url: string;
  model: string;
  details: string;
}

export interface ProviderMetrics {
  total_completions: number;
  avg_latency: number;
  p50_latency: number;
  p95_latency: number;
  avg_tokens_per_sec: number;
  json_failure_count: number;
  json_repair_count: number;
  fallback_trigger_count: number;
  grounding_pass_rate: number;
  passes_count: number;
  fails_count: number;
}

export function useProviderHealth() {
  const [health, setHealth] = useState<ProviderHealth | null>(null);
  const [metrics, setMetrics] = useState<ProviderMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = useCallback(async () => {
    try {
      setLoading(true);
      
      const healthRes = await fetch('/api/llm/health');
      const metricsRes = await fetch('/api/llm/metrics');
      
      if (!healthRes.ok || !metricsRes.ok) {
        throw new Error('Failed to retrieve active provider diagnostics profiles.');
      }
      
      const healthData = await healthRes.json();
      const metricsData = await metricsRes.json();
      
      setHealth(healthData);
      setMetrics(metricsData);
      setError(null);
    } catch (e: any) {
      setError(e.message || 'Error occurred querying LLM provider health status.');
    } finally {
      setLoading(false);
    }
  }, []);

  const triggerBenchmark = async () => {
    try {
      setLoading(true);
      const res = await fetch('/api/llm/benchmark', { method: 'POST' });
      if (!res.ok) {
        throw new Error('Inference benchmark execution rejected.');
      }
      await fetchStatus();
    } catch (e: any) {
      setError(e.message || 'Benchmark run failed.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 30000);
    return () => clearInterval(interval);
  }, [fetchStatus]);

  return { health, metrics, loading, error, refresh: fetchStatus, triggerBenchmark };
}
