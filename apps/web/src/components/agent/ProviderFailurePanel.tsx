"use client";

import React from 'react';
import { useProviderHealth } from '../../hooks/useProviderHealth';

export function ProviderFailurePanel() {
  const { metrics } = useProviderHealth();

  const totalCompletions = metrics?.total_completions || 0;
  const fallbacksCount = metrics?.fallback_trigger_count || 0;
  const jsonFailures = metrics?.json_failure_count || 0;
  const jsonRepairs = metrics?.json_repair_count || 0;
  const groundingPassRate = metrics?.grounding_pass_rate !== undefined ? metrics.grounding_pass_rate * 100 : 100;

  return (
    <div className="p-6 rounded-2xl bg-zinc-900/60 border border-zinc-800/80 backdrop-blur-md shadow-2xl flex flex-col space-y-6">
      <div>
        <h3 className="text-sm font-semibold text-zinc-100 tracking-wide font-mono">Failover & Structured Safety Logs</h3>
        <p className="text-xs text-zinc-500 mt-0.5">Summary of schema repairs and fallback failovers</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Fallbacks card */}
        <div className="p-4 rounded-xl bg-zinc-950/40 border border-zinc-900/80 flex flex-col">
          <span className="text-[10px] text-zinc-500 font-mono uppercase tracking-wider mb-1">Fallback triggers</span>
          <div className="flex items-baseline space-x-2">
            <span className="text-lg font-bold text-amber-400 font-mono">{fallbacksCount}</span>
            <span className="text-[10px] text-zinc-600 font-mono">/ {totalCompletions} calls</span>
          </div>
        </div>

        {/* JSON repairs card */}
        <div className="p-4 rounded-xl bg-zinc-950/40 border border-zinc-900/80 flex flex-col">
          <span className="text-[10px] text-zinc-500 font-mono uppercase tracking-wider mb-1">JSON repairs</span>
          <div className="flex items-baseline space-x-2">
            <span className="text-lg font-bold text-sky-400 font-mono">{jsonRepairs}</span>
            <span className="text-[10px] text-zinc-600 font-mono">/ {jsonFailures} errors</span>
          </div>
        </div>

        {/* Grounding pass rate */}
        <div className="p-4 rounded-xl bg-zinc-950/40 border border-zinc-900/80 flex flex-col">
          <span className="text-[10px] text-zinc-500 font-mono uppercase tracking-wider mb-1">Grounding Pass Rate</span>
          <div className="flex items-baseline space-x-2">
            <span className="text-lg font-bold text-emerald-400 font-mono">{groundingPassRate.toFixed(0)}%</span>
            <span className="text-[10px] text-zinc-600 font-mono">accuracy</span>
          </div>
        </div>
      </div>

      {/* Fallback detail warnings */}
      {fallbacksCount > 0 && (
        <div className="p-4 rounded-xl bg-amber-950/30 border border-amber-900/50 text-xs text-amber-300 font-mono space-y-2">
          <div className="font-semibold">[WARNING: ACTIVE FAILOVERS DETECTED]</div>
          <p className="text-[11px] text-amber-400/80 leading-relaxed">
            Local Ollama server timed out or returned malformed payloads. Requests were successfully 
            rerouted to standard cloud mock fallbacks. Check your &quot;ollama serve&quot; connection.
          </p>
        </div>
      )}

      {jsonRepairs > 0 && (
        <div className="p-4 rounded-xl bg-sky-950/30 border border-sky-900/50 text-xs text-sky-300 font-mono space-y-2">
          <div className="font-semibold">[INFO: STRUCTURAL OUTPUT REPAIRED]</div>
          <p className="text-[11px] text-sky-400/80 leading-relaxed">
            Local model produced malformed JSON brackets or commas. The StructuredOutputRepairService 
            intercepted, cleaned, and successfully restored compliance. No hard crashes triggered.
          </p>
        </div>
      )}
    </div>
  );
}
