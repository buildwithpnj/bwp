import { useState, useEffect } from 'react';

export interface GovernancePolicyLog {
  id: string;
  field_name: string;
  old_value: string;
  new_value: string;
  created_at: string;
}

export function useGovernanceConfig(tenantId: string) {
  const [history, setHistory] = useState<GovernancePolicyLog[]>([]);
  const [isUpdating, setIsUpdating] = useState(false);

  const fetchHistory = async () => {
    try {
      const res = await fetch(`/api/governance/audit-trail?tenant_id=${tenantId}`);
      if (res.ok) {
        const data = await res.json();
        setHistory(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    if (tenantId) {
      fetchHistory();
    }
  }, [tenantId]);

  const updatePolicy = async (fieldName: string, newValue: string) => {
    setIsUpdating(true);
    try {
      const res = await fetch('/api/governance/log-policy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tenant_id: tenantId, field_name: fieldName, new_value: newValue })
      });
      if (res.ok) {
        await fetchHistory();
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsUpdating(false);
    }
  };

  const toggleAgent = async (agentType: string, enabled: boolean) => {
    try {
      await fetch(`/api/governance/configure-agent?tenant_id=${tenantId}&agent_type=${agentType}&enabled=${enabled}`, {
        method: 'POST'
      });
    } catch (e) {
      console.error(e);
    }
  };

  const toggleAlert = async (ruleName: string, muted: boolean) => {
    try {
      await fetch(`/api/governance/configure-alert?tenant_id=${tenantId}&rule_name=${ruleName}&muted=${muted}`, {
        method: 'POST'
      });
    } catch (e) {
      console.error(e);
    }
  };

  return {
    history,
    isUpdating,
    updatePolicy,
    toggleAgent,
    toggleAlert
  };
}
