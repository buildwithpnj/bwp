'use client';

import { useState, useEffect } from 'react';
import { Brain, Sparkles, MessageSquare, Loader2, RefreshCw } from 'lucide-react';
import { api } from '@/lib/api';

interface CoachInsight {
  summary: string;
  content: string;
  completion_rate: number;
  total_habits: number;
  completed_today: number;
}

export default function AiCoachPage() {
  const [insight, setInsight] = useState<CoachInsight | null>(null);
  const [loading, setLoading] = useState(true);

  const loadInsight = async () => {
    setLoading(true);
    try {
      const data = await api<CoachInsight>('/api/aicoach/insights');
      setInsight(data);
    } catch (err) {
      console.error('Failed to load AI Coach insights:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInsight();
  }, []);

  return (
    <div className="space-y-6 animate-fade-in text-foreground h-[calc(100vh-80px)] overflow-hidden flex flex-col">
      {/* System Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">Cognitive Assistant</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <Brain className="h-7 w-7 text-primary" />
            AI Coach Companion
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Personal cognitive summaries, habits optimization, and wellness telemetry audits.
          </p>
        </div>

        <button
          onClick={loadInsight}
          className="p-2 hover:bg-accent rounded-lg border border-border transition-colors text-muted-foreground hover:text-foreground self-start md:self-auto"
          title="Regenerate review"
        >
          <RefreshCw className="h-4 w-4" />
        </button>
      </div>

      <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-6 overflow-hidden">
        
        {/* Core telemetry details */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4 h-fit">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-primary" />
            Today&apos;s Telemetry Audit
          </h3>

          {loading ? (
            <div className="py-8 text-center text-xs text-muted-foreground">Auditing database logs...</div>
          ) : insight ? (
            <div className="space-y-4 font-mono text-xs">
              <div className="flex justify-between border-b border-border/40 pb-2">
                <span className="text-muted-foreground">Habit Completion:</span>
                <span className="text-primary font-bold">{insight.completion_rate}%</span>
              </div>
              <div className="flex justify-between border-b border-border/40 pb-2">
                <span className="text-muted-foreground">Tasks Logged:</span>
                <span className="text-foreground">{insight.completed_today} / {insight.total_habits}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Focus State:</span>
                <span className={insight.completion_rate >= 50 ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold'}>
                  {insight.completion_rate >= 50 ? 'OPTIMIZED' : 'INCOMPLETE'}
                </span>
              </div>
            </div>
          ) : (
            <p className="text-xs text-muted-foreground">No metrics loaded.</p>
          )}
        </div>

        {/* Coach generated report */}
        <div className="md:col-span-2 rounded-2xl border border-border bg-card/30 p-6 flex flex-col justify-between overflow-y-auto">
          <div className="space-y-4">
            <div className="flex items-center gap-2.5 pb-3 border-b border-border">
              <MessageSquare className="h-5 w-5 text-primary" />
              <h4 className="text-sm font-semibold text-foreground">AI Daily Insights</h4>
            </div>

            {loading ? (
              <div className="py-12 flex flex-col items-center justify-center gap-3 text-muted-foreground">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
                <span className="text-xs">Auditing your Life OS database metrics…</span>
              </div>
            ) : insight ? (
              <p className="text-xs text-muted-foreground leading-relaxed font-mono bg-card/65 p-4 border border-border/60 rounded-xl">
                {insight.content}
              </p>
            ) : (
              <p className="text-xs text-muted-foreground">No insight report generated.</p>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
