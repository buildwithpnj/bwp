import { useState } from 'react';

export function useCanaryRollout() {
  const [percentage, setPercentage] = useState(10);
  const [status, setStatus] = useState('active');
  const [healthScore, setHealthScore] = useState(1.0);
  const [summary, setSummary] = useState('Rollout is healthy.');

  const updatePercentage = async (rolloutId: string, value: number) => {
    try {
      const res = await fetch(`/api/releases/canary/start?rollout_id=${rolloutId}&percentage=${value}`, { method: 'POST' });
      if (res.ok) {
        setPercentage(value);
        return true;
      }
    } catch (e) {
      console.error(e);
    }
    return false;
  };

  const updateStatus = async (rolloutId: string, action: string) => {
    try {
      const res = await fetch(`/api/releases/canary/${action}?rollout_id=${rolloutId}`, { method: 'POST' });
      if (res.ok) {
        if (action === 'pause') setStatus('paused');
        if (action === 'resume') setStatus('active');
        if (action === 'rollback') setStatus('rolled_back');
        return true;
      }
    } catch (e) {
      console.error(e);
    }
    return false;
  };

  const measureHealth = async (rolloutId: string) => {
    try {
      const res = await fetch(`/api/releases/health?rollout_id=${rolloutId}`);
      if (res.ok) {
        const data = await res.json();
        setHealthScore(data.health_score);
        setSummary(data.status_summary);
      }
    } catch (e) {
      console.error(e);
    }
  };

  return {
    percentage,
    status,
    healthScore,
    summary,
    updatePercentage,
    updateStatus,
    measureHealth
  };
}
