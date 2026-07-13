'use client';

import { useState } from 'react';

interface TenantControlsCardProps {
  onToggleAgent: (agentType: string, enabled: boolean) => void;
}

export function TenantControlsCard({ onToggleAgent }: TenantControlsCardProps) {
  const [agents, setAgents] = useState({
    research: true,
    diagnostics: true,
    execution: true
  });

  const handleToggle = (type: keyof typeof agents) => {
    const val = !agents[type];
    setAgents(prev => ({ ...prev, [type]: val }));
    onToggleAgent(type, val);
  };

  return (
    <div className="bg-muted/30 border border-border p-3.5 rounded-xl space-y-3">
      <h4 className="font-semibold text-foreground text-xs">Agent Capability Configuration</h4>
      
      <div className="space-y-2.5">
        {(Object.keys(agents) as Array<keyof typeof agents>).map(type => (
          <div key={type} className="flex items-center justify-between text-xs">
            <span className="capitalize text-foreground font-medium">{type} Agent</span>
            <button
              onClick={() => handleToggle(type)}
              className={`px-3 py-1 rounded text-[10px] font-semibold transition-all ${
                agents[type]
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  : 'bg-muted text-muted-foreground border border-border'
              }`}
            >
              {agents[type] ? 'Active' : 'Disabled'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
