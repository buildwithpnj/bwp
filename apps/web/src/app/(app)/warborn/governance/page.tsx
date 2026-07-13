'use client';

import { PolicySyncPanel } from '@/components/governance/PolicySyncPanel';
import { CanaryRolloutPanel } from '@/components/releases/CanaryRolloutPanel';
import { TelemetryOverviewPanel } from '@/components/ops/TelemetryOverviewPanel';
import { AnomalyIncidentFeed } from '@/components/ops/AnomalyIncidentFeed';
import { DegradedModePanel } from '@/components/resilience/DegradedModePanel';
import { OpsRiskOverview } from '@/components/analytics/OpsRiskOverview';
import { ShieldCheck, GitBranch } from 'lucide-react';

export default function FederatedGovernancePage() {
  return (
    <div className="space-y-6 animate-fade-in text-foreground text-left max-w-5xl mx-auto p-4">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-mono font-bold uppercase tracking-[0.25em] text-primary flex items-center gap-1">
            <ShieldCheck className="h-3 w-3" /> FEDERATED GOVERNANCE SYSTEMS
          </span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <GitBranch className="h-7 w-7 text-primary" />
            Federated Policy Sync & Rollout Control
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Manage cluster-wide policy drift syncs, environment gates, active canaries, and safety rollbacks.
          </p>
        </div>
      </div>

      {/* Main Grid panels */}
      <div className="space-y-6">
        <PolicySyncPanel />
        <CanaryRolloutPanel />
        
        {/* V37-V39 Observability, Resilience, and Risk Sections */}
        <TelemetryOverviewPanel />
        <AnomalyIncidentFeed />
        <DegradedModePanel />
        <OpsRiskOverview />
      </div>
    </div>
  );
}
