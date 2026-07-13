'use client';

import { useGovernanceConfig } from '@/hooks/useGovernanceConfig';
import { TenantControlsCard } from './TenantControlsCard';
import { AlertRulesEditor } from './AlertRulesEditor';
import { CopilotConfigPanel } from './CopilotConfigPanel';
import { PolicyChangePreview } from './PolicyChangePreview';

interface GovernancePanelProps {
  tenantId: string;
}

export function GovernancePanel({ tenantId }: GovernancePanelProps) {
  const { history, updatePolicy, toggleAgent, toggleAlert } = useGovernanceConfig(tenantId);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <TenantControlsCard onToggleAgent={toggleAgent} />
        <AlertRulesEditor onToggleAlert={toggleAlert} />
        <CopilotConfigPanel onUpdatePolicy={updatePolicy} />
      </div>

      <PolicyChangePreview logs={history} />
    </div>
  );
}
export default GovernancePanel;
