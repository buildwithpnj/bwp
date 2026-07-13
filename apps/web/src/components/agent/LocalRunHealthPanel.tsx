"use client";

import React from 'react';
import { useProviderHealth } from '../../hooks/useProviderHealth';

export function LocalRunHealthPanel() {
  const { health, metrics, loading, error, triggerBenchmark } = useProviderHealth();

  const statusColorText = {
    healthy: 'text-emerald-400',
    degraded: 'text-amber-400',
    offline: 'text-rose-400',
  };

  return (
    <div className="p-6 rounded-2xl bg-zinc-900/60 border border-zinc-800/80 backdrop-blur-md shadow-2xl flex flex-col space-y-6">
      <div className="flex items-center justify-between border-b border-zinc-800/60 pb-4">
        <div>
          <h3 className="text-sm font-semibold text-zinc-100 tracking-wide font-mono">Local Inference Diagnostics</h3>
          <p className="text-xs text-zinc-500 mt-0.5">Metrics layer auditing local Ollama server status</p>
        </div>
        <button
          onClick={triggerBenchmark}
          disabled={loading}
          className="px-3.5 py-1.5 rounded-lg bg-zinc-800 border border-zinc-700/60 text-xs font-mono text-zinc-200 hover:bg-zinc-750 transition-all disabled:opacity-50"
        >
          {loading ? 'Running Benchmark...' : 'Run Benchmark'}
        </button>
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-950/40 border border-rose-900/60 text-xs text-rose-300 font-mono">
          [CRITICAL ERROR]: {error}
        </div>
      )}

      {/* Grid of stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-zinc-950/40 border border-zinc-900/80 flex flex-col">
          <span className="text-[10px] text-zinc-500 font-mono uppercase tracking-wider mb-1">Status</span>
          <span className={`text-sm font-semibold font-mono ${statusColorText[health?.status || 'offline']}`}>
            {health?.status ? health.status.toUpperCase() : 'UNKNOWN'}
          </span>
        </div>

        <div className="p-4 rounded-xl bg-zinc-950/40 border border-zinc-900/80 flex flex-col">
          <span className="text-[10px] text-zinc-500 font-mono uppercase tracking-wider mb-1">Average Latency</span>
          <span className="text-sm font-semibold text-zinc-200 font-mono">
            {metrics?.avg_latency ? `${metrics.avg_latency.toFixed(2)}s` : '0.00s'}
          </span>
        </div>

        <div className="p-4 rounded-xl bg-zinc-950/40 border border-zinc-900/80 flex flex-col">
          <span className="text-[10px] text-zinc-500 font-mono uppercase tracking-wider mb-1">p95 Latency</span>
          <span className="text-sm font-semibold text-zinc-200 font-mono">
            {metrics?.p95_latency ? `${metrics.p95_latency.toFixed(2)}s` : '0.00s'}
          </span>
        </div>

        <div className="p-4 rounded-xl bg-zinc-950/40 border border-zinc-900/80 flex flex-col">
          <span className="text-[10px] text-zinc-500 font-mono uppercase tracking-wider mb-1">Speed</span>
          <span className="text-sm font-semibold text-zinc-200 font-mono">
            {metrics?.avg_tokens_per_sec ? `${metrics.avg_tokens_per_sec.toFixed(1)} t/s` : '0.0 t/s'}
          </span>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-zinc-950/30 border border-zinc-900/80 text-xs font-mono space-y-2.5">
        <div className="text-zinc-400 font-semibold border-b border-zinc-900 pb-1.5">Runtime Config details:</div>
        <div className="flex justify-between text-zinc-500">
          <span>Ollama Host URL:</span>
          <span className="text-zinc-300">{health?.base_url || 'http://localhost:11434'}</span>
        </div>
        <div className="flex justify-between text-zinc-500">
          <span>Active local model:</span>
          <span className="text-zinc-300">{health?.model || 'llama3'}</span>
        </div>
        <div className="flex justify-between text-zinc-500">
          <span>Llm Provider:</span>
          <span className="text-zinc-300">{health?.provider ? health.provider.toUpperCase() : 'OPENAI'}</span>
        </div>
      </div>
    </div>
  );
}
