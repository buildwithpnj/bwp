"use client";

import React from 'react';
import { useProviderHealth } from '../../hooks/useProviderHealth';

export function ProviderBadge() {
  const { health, loading } = useProviderHealth();

  if (loading && !health) {
    return (
      <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-zinc-900/50 border border-zinc-800 text-xs text-zinc-400 animate-pulse">
        <div className="w-2 h-2 rounded-full bg-zinc-600"></div>
        <span>polling core...</span>
      </div>
    );
  }

  const providerName = health?.provider || 'OpenAI';
  const modelName = health?.model || 'gpt-3.5-turbo';
  const status = health?.status || 'healthy';

  const statusColors = {
    healthy: 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.6)] border-emerald-400',
    degraded: 'bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.6)] border-amber-400',
    offline: 'bg-rose-500 shadow-[0_0_8px_rgba(239,68,68,0.6)] border-rose-400',
  };

  return (
    <div className="inline-flex items-center space-x-2.5 px-3.5 py-1.5 rounded-xl bg-zinc-950/70 border border-zinc-800/80 backdrop-blur-md shadow-inner text-xs font-mono tracking-wider transition-all duration-300">
      <div className="relative flex items-center">
        <span className={`w-2 h-2 rounded-full border ${statusColors[status]}`} />
      </div>
      <div className="flex flex-col text-left">
        <span className="text-[10px] text-zinc-500 uppercase tracking-widest leading-none mb-0.5">{providerName}</span>
        <span className="text-zinc-200 font-semibold leading-none">{modelName}</span>
      </div>
    </div>
  );
}
