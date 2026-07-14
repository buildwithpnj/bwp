'use client';

import { Terminal as TerminalIcon, Cpu, PlayCircle, Layers, Activity, Server } from 'lucide-react';

export default function WorkspacePage() {
  return (
    <div className="space-y-6 animate-fade-in text-foreground">
      {/* System Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">Core Kernel</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <TerminalIcon className="h-7 w-7 text-primary" />
            Developer Workspace
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Active subprocess controls, runtime telemetry monitors, and background workers.
          </p>
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* active status */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Server className="h-4 w-4 text-primary" />
            Daemon Services
          </h3>
          <div className="space-y-3 font-mono text-2xs">
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span className="text-muted-foreground">api-server:</span>
              <span className="text-emerald-400 font-semibold flex items-center gap-1">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" /> RUNNING (Port 8000)
              </span>
            </div>
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span className="text-muted-foreground">web-server:</span>
              <span className="text-emerald-400 font-semibold flex items-center gap-1">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" /> RUNNING (Port 3000)
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">redis-cache:</span>
              <span className="text-emerald-400 font-semibold flex items-center gap-1">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" /> ONLINE
              </span>
            </div>
          </div>
        </div>

        {/* task runner */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Cpu className="h-4 w-4 text-primary" />
            Telemetry Metrics
          </h3>
          <div className="space-y-3 font-mono text-2xs">
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span className="text-muted-foreground">CPU Usage:</span>
              <span className="text-foreground">4.2%</span>
            </div>
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span className="text-muted-foreground">RAM Allocated:</span>
              <span className="text-foreground">248 MB</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Database Pool:</span>
              <span className="text-foreground">8 / 20 active</span>
            </div>
          </div>
        </div>

        {/* pipeline */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Layers className="h-4 w-4 text-primary" />
            Integrations Pipeline
          </h3>
          <div className="space-y-3 font-mono text-2xs text-muted-foreground">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              <span>Alembic database upgrades applied.</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              <span>Google Drive OAuth secrets encrypted.</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-blue-400" />
              <span>Drive B failover target seed synced.</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
