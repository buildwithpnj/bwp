'use client';

import { useResilienceState } from '@/hooks/useResilienceState';
import { ResilienceStatusBanner } from './ResilienceStatusBanner';
import { FallbackDecisionCard } from './FallbackDecisionCard';
import { RecoveryTimeline } from './RecoveryTimeline';

export function DegradedModePanel() {
  const { resilienceState, history, manuallyActivateDegraded, manualOverride, refresh } = useResilienceState();

  const handleManualDegradation = async () => {
    await manuallyActivateDegraded('chat_copilot', 'cached_summaries', 'voice_audio');
  };

  return (
    <div className="bg-background border border-border p-5 rounded-xl space-y-6">
      <div className="border-b border-border pb-2 flex items-center justify-between">
        <h3 className="font-semibold text-foreground text-xs">Resilience & Degraded-Mode Operations</h3>
        <button
          onClick={refresh}
          className="text-primary hover:underline text-[10px] font-semibold"
        >
          Refresh State
        </button>
      </div>

      <ResilienceStatusBanner level={resilienceState?.degradation_level ?? 'normal'} />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-4 text-xs">
          <p className="text-[10px] text-muted-foreground leading-normal">
            Gracefully switches non-critical systems to lower budget fallbacks during provider timeouts.
          </p>
          <div className="flex gap-2">
            <button
              onClick={handleManualDegradation}
              className="bg-muted hover:bg-accent border border-border px-3 py-1.5 rounded-md font-semibold text-foreground flex-1"
            >
              Trigger Degraded Mode
            </button>
            <button
              onClick={manualOverride}
              className="bg-primary text-primary-foreground hover:bg-primary/95 px-3 py-1.5 rounded-md font-semibold flex-1"
            >
              Override / Clear
            </button>
          </div>
        </div>

        <FallbackDecisionCard />
      </div>

      <RecoveryTimeline history={history} />
    </div>
  );
}
export default DegradedModePanel;
