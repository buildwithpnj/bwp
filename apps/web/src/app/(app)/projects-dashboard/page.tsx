'use client';

import { Briefcase, FolderKanban, CheckSquare, FileText, Settings, Rocket } from 'lucide-react';

export default function ProjectsPage() {
  return (
    <div className="space-y-6 animate-fade-in text-foreground">
      {/* System Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">Active Operations</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <Briefcase className="h-7 w-7 text-primary" />
            Projects & Operations
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Linear-style tracking of active projects, timeline tasks, repository documents, and deployment states.
          </p>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* Project Folders */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <FolderKanban className="h-4 w-4 text-primary" />
            Active Folders
          </h3>
          <div className="space-y-2 text-xs font-mono">
            {[
              { name: 'warborn-refactor-v2', count: '14 files', status: 'ACTIVE' },
              { name: 'google-oauth-multi-drive', count: '8 files', status: 'COMPLETED' },
            ].map((proj, idx) => (
              <div key={idx} className="flex justify-between border-b border-border/40 pb-2">
                <span className="font-semibold text-foreground">/{proj.name}</span>
                <div className="flex items-center gap-2">
                  <span className="text-muted-foreground text-3xs">{proj.count}</span>
                  <span className={`text-3xs px-1.5 rounded-sm ${
                    proj.status === 'ACTIVE' ? 'bg-amber-500/10 text-amber-500' : 'bg-emerald-500/10 text-emerald-500'
                  }`}>{proj.status}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Task Board summary */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <CheckSquare className="h-4 w-4 text-primary" />
            Operational Tasks
          </h3>
          <div className="space-y-2.5 text-xs">
            {[
              { title: 'Define custom types for B-drive callback payload', progress: 'In Review' },
              { title: 'Integrate dynamic client ID logic into oauth managers', progress: 'Done' },
              { title: 'Refactor storage page lists into manager columns', progress: 'Done' },
            ].map((task, idx) => (
              <div key={idx} className="flex items-center justify-between border-b border-border/40 pb-2">
                <span className="truncate font-semibold text-foreground max-w-[200px]">{task.title}</span>
                <span className="text-3xs rounded px-1.5 bg-muted font-mono">{task.progress}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Deployment Status */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Rocket className="h-4 w-4 text-primary" />
            System Deployments
          </h3>
          <div className="space-y-3 font-mono text-2xs">
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span className="text-muted-foreground">Local Cluster:</span>
              <span className="text-emerald-400 font-semibold">ONLINE (127.0.0.1)</span>
            </div>
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span className="text-muted-foreground">Environment:</span>
              <span className="text-foreground">Development (local)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Main DB Schema:</span>
              <span className="text-foreground">alembic-head (active)</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
