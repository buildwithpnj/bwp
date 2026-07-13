'use client';

import { useCanaryRollout } from '@/hooks/useCanaryRollout';
import { ReleaseGatePanel } from './ReleaseGatePanel';
import { RolloutHealthCard } from './RolloutHealthCard';
import { RolloutDecisionTimeline } from './RolloutDecisionTimeline';

export function CanaryRolloutPanel() {
  const rolloutId = 'roll_canary_123';
  const { percentage, status, healthScore, summary, updatePercentage, updateStatus, measureHealth } = useCanaryRollout();

  const handlePercentageChange = async (val: number) => {
    await updatePercentage(rolloutId, val);
  };

  const handleAction = async (action: string) => {
    await updateStatus(rolloutId, action);
  };

  return (
    <div className="bg-background border border-border p-5 rounded-xl space-y-6">
      <div className="border-b border-border pb-2 flex items-center justify-between">
        <h3 className="font-semibold text-foreground text-xs">Canary Rollouts & Safety Controls</h3>
        <span className="text-[10px] text-muted-foreground font-mono">Rollout ID: {rolloutId}</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Left Column: Progress Slider & Controls */}
        <div className="space-y-4 text-xs">
          <div className="flex justify-between items-center">
            <span className="text-muted-foreground font-medium">Canary Exposure</span>
            <span className="text-foreground font-bold">{percentage}%</span>
          </div>

          <input
            type="range"
            min="10"
            max="100"
            step="10"
            value={percentage}
            onChange={e => handlePercentageChange(Number(e.target.value))}
            className="w-full h-1 bg-muted rounded-lg appearance-none cursor-pointer accent-primary"
          />

          <div className="flex gap-2 justify-between">
            <span className="text-[10px] text-muted-foreground">Status: <span className="font-semibold text-foreground capitalize">{status}</span></span>
            <button
              onClick={() => measureHealth(rolloutId)}
              className="text-primary hover:underline text-[10px] font-semibold"
            >
              Recalculate Health
            </button>
          </div>

          <div className="flex gap-2.5 pt-2">
            <button
              onClick={() => handleAction('pause')}
              className="bg-muted hover:bg-accent border border-border px-3 py-1.5 rounded-md font-semibold flex-1"
            >
              Pause
            </button>
            <button
              onClick={() => handleAction('resume')}
              className="bg-muted hover:bg-accent border border-border px-3 py-1.5 rounded-md font-semibold flex-1"
            >
              Resume
            </button>
            <button
              onClick={() => handleAction('rollback')}
              className="bg-red-500/20 text-red-400 hover:bg-red-500/35 border border-red-500/30 px-3 py-1.5 rounded-md font-semibold flex-1"
            >
              Rollback
            </button>
          </div>
        </div>

        {/* Right Column: Health Telemetry Score Card */}
        <RolloutHealthCard healthScore={healthScore} summary={summary} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-border/40">
        <ReleaseGatePanel rolloutId={rolloutId} onApprove={() => alert('Approval Signature Registered.')} />
        <RolloutDecisionTimeline percentage={percentage} status={status} />
      </div>
    </div>
  );
}
export default CanaryRolloutPanel;
