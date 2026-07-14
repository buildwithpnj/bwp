'use client';

import { useState, useEffect } from 'react';
import { 
  CheckSquare, 
  HardDrive, 
  Calendar as CalendarIcon, 
  FileText, 
  Cpu, 
  Activity, 
  ShieldCheck,
  Flame,
  Brain,
  MessageSquare,
  Sparkles,
  ArrowUpRight,
  Target,
  Globe
} from 'lucide-react';
import Link from 'next/link';
import { api } from '@/lib/api';

interface StorageProvider {
  provider_label: string;
  account_email: string;
  connected: boolean;
  status: string;
}

interface Habit {
  id: string;
  name: string;
  logs: { date: string }[];
}

interface CalendarEvent {
  id: string;
  title: string;
  start_time: string;
}

interface Addiction {
  id: string;
  name: string;
  current_streak_days: number;
  money_saved?: number;
  time_saved_hours?: number;
}

interface CoachInsight {
  content: string;
  completion_rate: number;
}

interface GeoInfo {
  country_name: string;
  country_code: string;
  currency: string;
  timezone: string;
}

interface MemoryProgress {
  corrections_accepted: number;
  streak: number;
  weak_categories: string[];
  mastered_patterns: string[];
}

const currencySymbols: Record<string, string> = {
  USD: '$',
  INR: '₹',
  GBP: '£',
  JPY: '¥',
  EUR: '€',
};

const getBrowserGeo = (): GeoInfo => {
  const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
  let code = 'US';
  let name = 'United States';
  let curr = 'USD';
  
  if (tz.includes('Kolkata') || tz.includes('India') || tz.includes('Asia/Calcutta')) {
    code = 'IN';
    name = 'India';
    curr = 'INR';
  } else if (tz.includes('London') || tz.includes('Europe/London')) {
    code = 'GB';
    name = 'United Kingdom';
    curr = 'GBP';
  } else if (tz.includes('Tokyo') || tz.includes('Asia/Tokyo')) {
    code = 'JP';
    name = 'Japan';
    curr = 'JPY';
  }
  return { country_name: name, country_code: code, currency: curr, timezone: tz };
};

export default function MissionControlPage() {
  const [time, setTime] = useState<string>('');
  const [providers, setProviders] = useState<StorageProvider[]>([]);
  const [habits, setHabits] = useState<Habit[]>([]);
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [addictions, setAddictions] = useState<Addiction[]>([]);
  const [insight, setInsight] = useState<CoachInsight | null>(null);
  const [geo, setGeo] = useState<GeoInfo | null>(null);
  const [memoryProgress, setMemoryProgress] = useState<MemoryProgress | null>(null);
  const [loading, setLoading] = useState(true);

  // Time ticker
  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const options: Intl.DateTimeFormatOptions = {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
      };
      if (geo?.timezone) {
        options.timeZone = geo.timezone;
      }
      setTime(now.toLocaleTimeString([], options));
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, [geo]);

  // Geo detection API
  useEffect(() => {
    async function detectGeo() {
      try {
        const res = await fetch('https://ipapi.co/json/');
        if (res.ok) {
          const data = await res.json();
          setGeo({
            country_name: data.country_name || 'United States',
            country_code: data.country_code || 'US',
            currency: data.currency || 'USD',
            timezone: data.timezone || 'America/New_York',
          });
        } else {
          setGeo(getBrowserGeo());
        }
      } catch {
        setGeo(getBrowserGeo());
      }
    }
    detectGeo();
  }, []);

  const loadData = async () => {
    try {
      const stData = await api<{ providers: StorageProvider[] }>('/api/storage/providers');
      setProviders(stData.providers || []);

      const hData = await api<Habit[]>('/api/habits');
      setHabits(hData?.slice(0, 4) || []);

      const cData = await api<CalendarEvent[]>('/api/gcalendar/events');
      setEvents(cData?.slice(0, 3) || []);

      const aData = await api<Addiction[]>('/api/recovery/addictions');
      setAddictions(aData?.slice(0, 3) || []);

      const iData = await api<CoachInsight>('/api/aicoach/insights');
      setInsight(iData);

      const mData = await api<MemoryProgress>('/api/memory/progress');
      setMemoryProgress(mData);
    } catch (err) {
      console.error('Failed to load Mission Control telemetry:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const toggleHabitLog = async (h: Habit) => {
    const todayStr = new Date().toISOString().split('T')[0];
    const logged = h.logs?.some((l) => l.date === todayStr);
    try {
      await api(`/api/habits/${h.id}/log`, {
        method: 'POST',
        body: {
          date: todayStr,
          value: logged ? 0.0 : 1.0,
        },
      });
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const getTodayEvents = () => {
    const todayStr = new Date().toISOString().split('T')[0];
    return events.filter(e => e.start_time.startsWith(todayStr));
  };
  const todayEvents = getTodayEvents();

  return (
    <div className="space-y-6 animate-fade-in text-pnj-textStrong font-sans">
      {/* Monospace Header telemetry strip */}
      <div className="flex items-center justify-between border-b border-border pb-3">
        <div>
          <span className="font-mono text-[10px] tracking-[0.25em] text-primary uppercase font-bold">SYSTEM_COCKPIT // v0.50.1</span>
          <h1 className="text-xl font-bold tracking-tight mt-0.5">MISSION CONTROL</h1>
        </div>
        <div className="hidden md:flex items-center gap-4 font-mono text-[11px] text-muted-foreground">
          <span>CLOCK: {time || '--:--:--'}</span>
          <span className="opacity-30">|</span>
          <span>TZ: {geo?.timezone || 'UTC'}</span>
        </div>
      </div>

      {/* Main Grid: Three structural columns */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Column 1: Focus Canopy */}
        <div className="lg:col-span-2 border border-border bg-card p-5 flex flex-col justify-between min-h-[340px]">
          <div>
            <div className="flex items-center justify-between border-b border-border/40 pb-2 mb-4">
              <h2 className="text-xs font-bold uppercase tracking-wider text-muted-foreground font-mono">
                01 // FOCUS_CANOPY
              </h2>
              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 uppercase font-bold">
                ACTIVE_RUN
              </span>
            </div>

            <div className="space-y-4">
              <div>
                <span className="font-mono text-[10px] text-muted-foreground uppercase">CURRENT_MISSION:</span>
                <h3 className="text-lg font-bold text-foreground mt-0.5 leading-snug">
                  Optimize API Gateway Routing & Gating Tokens Policy
                </h3>
                <p className="text-xs text-muted-foreground mt-1">
                  Primary execution block for Warborn Copilot V0.50.1 safety audit.
                </p>
              </div>

              {/* Parsed AI Warning strip */}
              <div className="border border-amber-500/20 bg-amber-500/5 p-3 flex items-start gap-2.5">
                <span className="font-mono text-[10px] text-amber-500 uppercase font-bold shrink-0 mt-0.5">
                  [!] ALERT:
                </span>
                <p className="text-xs text-amber-200/80 leading-relaxed font-mono">
                  You have 2 pending action approvals blocking execution of task cleanups. Use Copilot drawer to resolve.
                </p>
              </div>
            </div>
          </div>

          {/* Timeline Excerpts */}
          <div className="mt-6 pt-4 border-t border-border/40">
            <span className="font-mono text-[10px] text-muted-foreground uppercase block mb-2">NEXT_SCHEDULE_TIMELINE:</span>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {loading ? (
                <p className="text-3xs text-muted-foreground italic font-mono">Syncing calendar timelines...</p>
              ) : todayEvents.length === 0 ? (
                <p className="text-3xs text-muted-foreground italic font-mono col-span-3">No events scheduled today.</p>
              ) : (
                todayEvents.slice(0, 3).map((evt) => (
                  <div key={evt.id} className="border border-border/60 bg-muted/10 p-2.5 font-mono">
                    <span className="text-[10px] text-primary font-bold block">
                      {new Date(evt.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false })}
                    </span>
                    <span className="text-xs text-foreground mt-0.5 block truncate">{evt.title}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Column 2: Goals, Habits & Recovery Stream */}
        <div className="border border-border bg-card p-5 space-y-4 flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-center pb-2 border-b border-border/40 mb-4">
              <h2 className="text-xs font-bold uppercase tracking-wider text-muted-foreground font-mono">
                02 // ROUTINE_FLOW
              </h2>
              <Link href="/habits" className="text-3xs text-primary hover:underline font-mono">FLOWS</Link>
            </div>

            {/* List Panels (No cards) */}
            <div className="space-y-3 font-mono">
              <span className="text-[10px] text-muted-foreground uppercase block">TODAY_HABITS_CHECKLIST:</span>
              <div className="border border-border/60 divide-y divide-border/60">
                {loading ? (
                  <p className="text-3xs text-muted-foreground italic p-3">Auditing logs...</p>
                ) : habits.length === 0 ? (
                  <p className="text-3xs text-muted-foreground italic p-3">No active habits.</p>
                ) : (
                  habits.slice(0, 3).map((h) => {
                    const todayStr = new Date().toISOString().split('T')[0];
                    const checked = h.logs?.some((l) => l.date === todayStr);

                    return (
                      <button
                        key={h.id}
                        onClick={() => toggleHabitLog(h)}
                        className="w-full flex items-center justify-between p-2.5 text-left hover:bg-muted/10 text-xs transition-colors"
                      >
                        <span className={`truncate ${checked ? 'line-through text-muted-foreground' : 'text-foreground'}`}>
                          {h.name.toUpperCase()}
                        </span>
                        <span className={`text-[10px] font-bold ${checked ? 'text-primary' : 'text-muted-foreground'}`}>
                          {checked ? '[X]' : '[ ]'}
                        </span>
                      </button>
                    );
                  })
                )}
              </div>
            </div>

            {/* Recovery Streaks */}
            <div className="mt-5 space-y-3 font-mono">
              <span className="text-[10px] text-muted-foreground uppercase block">SOBRIETY_RECOVERY_STREAKS:</span>
              <div className="border border-border/60 divide-y divide-border/60">
                {loading ? (
                  <p className="text-3xs text-muted-foreground italic p-3">Reading streak registers...</p>
                ) : addictions.length === 0 ? (
                  <p className="text-3xs text-muted-foreground italic p-3">No active trackers.</p>
                ) : (
                  addictions.slice(0, 2).map((add) => (
                    <div key={add.id} className="flex justify-between items-center p-2.5 text-xs">
                      <span className="truncate">{add.name.toUpperCase()}</span>
                      <span className="text-primary font-bold text-sm shrink-0">{add.current_streak_days}D</span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Combined Streak Metrics */}
          <div className="border-t border-border/40 pt-4 flex justify-between items-center text-[10px] font-mono text-muted-foreground">
            <span>STREAK: 12 DAYS</span>
            <span>SAVED: {currencySymbols[geo?.currency || 'USD'] || '$'}{addictions[0]?.money_saved || 240}</span>
          </div>
        </div>

        {/* Column 3: System Health & Quick Action Command Input */}
        <div className="border border-border bg-card p-5 space-y-4 flex flex-col justify-between lg:col-span-3 xl:col-span-1">
          <div>
            <div className="flex justify-between items-center pb-2 border-b border-border/40 mb-4">
              <h2 className="text-xs font-bold uppercase tracking-wider text-muted-foreground font-mono">
                03 // DIAGNOSTICS
              </h2>
              <span className="text-[9px] font-mono text-muted-foreground uppercase">NODE_ONLINE</span>
            </div>

            {/* System Status Table */}
            <div className="space-y-3 font-mono text-xs">
              <div className="border border-border/60 divide-y divide-border/60">
                <div className="flex justify-between items-center p-2.5">
                  <span className="text-3xs text-muted-foreground uppercase">KERNEL_LATENCY</span>
                  <span className="text-emerald-400 font-bold">14 MS</span>
                </div>
                <div className="flex justify-between items-center p-2.5">
                  <span className="text-3xs text-muted-foreground uppercase">SECURE_CRYPTOGRAPHY</span>
                  <span className="text-sky-400 font-bold">AES-256</span>
                </div>
                <div className="flex justify-between items-center p-2.5">
                  <span className="text-3xs text-muted-foreground uppercase">DRIVE_HEALTH</span>
                  <span className="text-foreground">ONLINE</span>
                </div>
                <div className="flex justify-between items-center p-2.5">
                  <span className="text-3xs text-muted-foreground uppercase">MEMORY_STREAK</span>
                  <span className="text-primary font-bold">{memoryProgress?.streak || 5} DAYS</span>
                </div>
              </div>
            </div>

            {/* Coach Insight */}
            <div className="mt-5 space-y-2">
              <span className="font-mono text-[10px] text-muted-foreground uppercase block">COGNITIVE_COACH_LOG:</span>
              <p className="text-xs text-muted-foreground font-mono leading-relaxed bg-muted/10 p-3 border border-border/60 italic">
                {insight ? `"${insight.content}"` : '"Maintain API telemetry checks weekly. Core system is stable."'}
              </p>
            </div>
          </div>

          {/* Quick Action Input Strip */}
          <div className="border border-border bg-pnj-bg flex items-center px-3 py-2 font-mono text-xs">
            <span className="text-primary mr-2 font-bold">&gt;</span>
            <input 
              type="text" 
              placeholder="ENTER COMMAND OR INTENT ACTION..." 
              className="w-full bg-transparent outline-none border-none text-foreground placeholder:text-muted-foreground uppercase tracking-wide font-mono text-[11px]"
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  const val = e.currentTarget.value.trim();
                  if (val) {
                    // Open keyboard command palette or broadcast command
                    window.dispatchEvent(new CustomEvent('copilot-input', { detail: val }));
                    e.currentTarget.value = '';
                  }
                }
              }}
            />
          </div>
        </div>

      </div>
    </div>
  );
}
