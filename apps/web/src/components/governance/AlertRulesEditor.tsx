'use client';

import { useState } from 'react';

interface AlertRulesEditorProps {
  onToggleAlert: (ruleName: string, muted: boolean) => void;
}

export function AlertRulesEditor({ onToggleAlert }: AlertRulesEditorProps) {
  const [rules, setRules] = useState({
    quota_warning: false,
    checkpoint_failed: false,
    simulation_anomaly: false
  });

  const handleToggle = (rule: keyof typeof rules) => {
    const val = !rules[rule];
    setRules(prev => ({ ...prev, [rule]: val }));
    onToggleAlert(rule, val);
  };

  return (
    <div className="bg-muted/30 border border-border p-3.5 rounded-xl space-y-3">
      <h4 className="font-semibold text-foreground text-xs">Mute Alert Rules</h4>
      
      <div className="space-y-2.5">
        {(Object.keys(rules) as Array<keyof typeof rules>).map(rule => (
          <div key={rule} className="flex items-center justify-between text-xs">
            <span className="text-foreground font-medium">{rule.replace('_', ' ')}</span>
            <button
              onClick={() => handleToggle(rule)}
              className={`px-3 py-1 rounded text-[10px] font-semibold transition-all ${
                rules[rule]
                  ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                  : 'bg-muted text-muted-foreground border border-border'
              }`}
            >
              {rules[rule] ? 'Muted' : 'Notify'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
