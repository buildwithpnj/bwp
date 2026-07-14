'use client';

import React, { useState } from 'react';
import { Briefcase, FolderKanban, CheckSquare, Rocket, Calendar, Target, Flame, Activity } from 'lucide-react';

export default function ProjectsPage() {
  const [missionsView, setMissionsView] = useState<'projects' | 'timeline' | 'rhythm'>('projects');

  return (
    <div className="space-y-6 animate-fade-in text-pnj-textStrong font-sans">
      {/* Page Header */}
      <div className="flex items-center justify-between border-b border-border pb-3">
        <div>
          <span className="font-mono text-[10px] tracking-[0.25em] text-primary uppercase font-bold">SYSTEM_MISSIONS // TEMPORAL_TRACKING</span>
          <h1 className="text-xl font-bold tracking-tight mt-0.5">MISSIONS</h1>
        </div>
        <div className="flex gap-2">
          {['projects', 'timeline', 'rhythm'].map((view) => (
            <button
              key={view}
              onClick={() => setMissionsView(view as any)}
              className={`px-3 py-1 border transition-colors uppercase font-mono font-bold text-[10px] ${
                missionsView === view
                  ? 'text-primary border-primary bg-primary/5'
                  : 'text-muted-foreground border-border hover:border-muted-foreground'
              }`}
            >
              {view}
            </button>
          ))}
        </div>
      </div>

      {/* Conditional Renderer */}
      {missionsView === 'projects' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          {/* Active Folders */}
          <div className="border border-border bg-card p-5 space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2 font-mono pb-2 border-b border-border/40">
              <FolderKanban className="h-4 w-4 text-primary" />
              01 // ACTIVE_FOLDERS
            </h3>
            <div className="space-y-2.5 text-xs font-mono">
              {[
                { name: 'warborn-refactor-v2', count: '14 files', status: 'ACTIVE' },
                { name: 'google-oauth-multi-drive', count: '8 files', status: 'COMPLETED' },
              ].map((proj, idx) => (
                <div key={idx} className="flex justify-between border-b border-border/40 pb-2">
                  <span className="font-semibold text-foreground">/{proj.name}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-muted-foreground text-3xs">{proj.count}</span>
                    <span className={`text-3xs px-1.5 border ${
                      proj.status === 'ACTIVE' ? 'border-amber-500/20 bg-amber-500/5 text-amber-500' : 'border-emerald-500/20 bg-emerald-500/5 text-emerald-400'
                    }`}>{proj.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Operational Tasks */}
          <div className="border border-border bg-card p-5 space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2 font-mono pb-2 border-b border-border/40">
              <CheckSquare className="h-4 w-4 text-primary" />
              02 // OPERATION_TASKS
            </h3>
            <div className="space-y-2.5 text-xs font-mono">
              {[
                { title: 'Define custom types for B-drive callback payload', progress: 'IN_REVIEW' },
                { title: 'Integrate dynamic client ID logic into oauth managers', progress: 'DONE' },
                { title: 'Refactor storage page lists into manager columns', progress: 'DONE' },
              ].map((task, idx) => (
                <div key={idx} className="flex items-center justify-between border-b border-border/40 pb-2">
                  <span className="truncate text-foreground max-w-[180px]">{task.title.toUpperCase()}</span>
                  <span className={`text-3xs px-1.5 border ${
                    task.progress === 'DONE' ? 'border-emerald-500/20 bg-emerald-500/5 text-emerald-400' : 'border-border bg-muted/20 text-muted-foreground'
                  }`}>{task.progress}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Cluster Status */}
          <div className="border border-border bg-card p-5 space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2 font-mono pb-2 border-b border-border/40">
              <Rocket className="h-4 w-4 text-primary" />
              03 // CLUSTER_TELEMETRY
            </h3>
            <div className="space-y-3 font-mono text-2xs">
              <div className="flex justify-between border-b border-border/40 pb-2">
                <span className="text-muted-foreground">Local Node:</span>
                <span className="text-emerald-400 font-semibold">ONLINE (127.0.0.1)</span>
              </div>
              <div className="flex justify-between border-b border-border/40 pb-2">
                <span className="text-muted-foreground">Environment:</span>
                <span className="text-foreground">Development</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Main Schema:</span>
                <span className="text-foreground">alembic-head (active)</span>
              </div>
            </div>
          </div>

        </div>
      )}

      {/* Timeline view (Calendar merged) */}
      {missionsView === 'timeline' && (
        <div className="border border-border bg-card p-5 space-y-4 font-mono text-xs">
          <div className="flex items-center justify-between border-b border-border/40 pb-2 mb-2">
            <span className="text-[10px] text-muted-foreground uppercase font-bold">12_HOUR_TIMELINE</span>
            <span className="text-[10px] text-primary">DATE: {new Date().toISOString().split('T')[0]}</span>
          </div>

          <div className="relative border-l border-border/60 ml-4 pl-6 space-y-6">
            {[
              { time: '09:00', title: 'Daily sync and task priority routing' },
              { time: '11:30', title: 'Hardening API security gating test runs' },
              { time: '14:00', title: 'Cortex indexing sync checks' },
              { time: '16:30', title: 'Vault storage connectivity audit' }
            ].map((event, idx) => (
              <div key={idx} className="relative">
                <span className="absolute -left-[31px] top-0.5 h-2 w-2 rounded-full bg-primary border-4 border-card" />
                <span className="text-[10px] text-primary font-bold">{event.time}</span>
                <p className="text-foreground mt-0.5 text-xs font-sans">{event.title}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Rhythm view (Habits merged) */}
      {missionsView === 'rhythm' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="border border-border bg-card p-5 space-y-4 font-mono text-xs">
            <div className="flex items-center justify-between border-b border-border/40 pb-2">
              <span className="text-[10px] text-muted-foreground uppercase font-bold">DAILY_HABITS</span>
              <span className="text-[10px] text-emerald-400">STREAK: 12 DAYS</span>
            </div>
            <div className="border border-border/60 divide-y divide-border/60">
              {[
                { name: 'Write 500 words of engineering design docs', done: true },
                { name: 'Review API telemetry and access audits', done: true },
                { name: 'Check secondary Vault backup node syncs', done: false }
              ].map((habit, i) => (
                <div key={i} className="flex justify-between items-center p-2.5 text-xs">
                  <span className={habit.done ? 'line-through text-muted-foreground font-sans' : 'text-foreground font-sans'}>
                    {habit.name.toUpperCase()}
                  </span>
                  <span className={habit.done ? 'text-primary font-bold' : 'text-muted-foreground'}>
                    {habit.done ? '[X]' : '[ ]'}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="border border-border bg-card p-5 space-y-4 font-mono text-xs">
            <div className="flex items-center justify-between border-b border-border/40 pb-2">
              <span className="text-[10px] text-muted-foreground uppercase font-bold">SOBRIETY_RECOVERY</span>
              <span className="text-[10px] text-primary">SAVINGS TRACKER</span>
            </div>
            <div className="border border-border/60 divide-y divide-border/60">
              {[
                { trigger: 'Nicotine Free', streak: '12d', saved: '$240 saved' },
                { trigger: 'Caffeine Limit', streak: '8d', saved: '$45 saved' }
              ].map((recovery, i) => (
                <div key={i} className="flex justify-between items-center p-2.5 text-xs">
                  <div>
                    <span className="block text-foreground font-sans">{recovery.trigger.toUpperCase()}</span>
                    <span className="text-[10px] text-muted-foreground font-mono">{recovery.saved}</span>
                  </div>
                  <span className="text-primary font-bold text-sm">{recovery.streak}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
