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
    <div className="space-y-6 animate-fade-in text-foreground">
      {/* System Telemetry Cockpit Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">System Cockpit</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1">Mission Control</h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Operational cockpit monitoring schedules, cloud storage health, routines, and wellness insights.
          </p>
        </div>

        {/* Telemetry readouts */}
        <div className="flex items-center gap-6 text-xs font-mono">
          {geo && (
            <>
              <div className="hidden md:flex flex-col text-right">
                <span className="text-3xs uppercase text-muted-foreground tracking-wider">Regional Node</span>
                <span className="text-sm font-semibold text-primary flex items-center gap-1.5 justify-end">
                  <Globe className="h-3.5 w-3.5 text-primary" />
                  <span>{geo.country_code} Node</span>
                </span>
              </div>
              <div className="h-8 w-px bg-border hidden md:block" />
            </>
          )}
          <div className="hidden sm:flex flex-col text-right">
            <span className="text-3xs uppercase text-muted-foreground tracking-wider">System Clock</span>
            <span className="text-sm font-semibold tabular-nums text-foreground">{time || '--:--:--'}</span>
          </div>
          <div className="h-8 w-px bg-border hidden sm:block" />
          <div className="flex flex-col">
            <span className="text-3xs uppercase text-muted-foreground tracking-wider">Kernel Latency</span>
            <span className="text-sm font-semibold text-emerald-400 flex items-center gap-1">
              <Activity className="h-3.5 w-3.5 text-emerald-400 animate-pulse" /> 14 ms
            </span>
          </div>
          <div className="h-8 w-px bg-border" />
          <div className="flex flex-col">
            <span className="text-3xs uppercase text-muted-foreground tracking-wider">Secure Cryptography</span>
            <span className="text-sm font-semibold text-sky-400 flex items-center gap-1">
              <ShieldCheck className="h-3.5 w-3.5 text-sky-400" /> AES-256
            </span>
          </div>
        </div>
      </div>

      {/* Main Grid dashboard layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* Today's Habits Checklist */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <div className="flex justify-between items-center pb-2 border-b border-border/40">
            <h2 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
              <Target className="h-4 w-4 text-primary" />
              Today&apos;s Habits
            </h2>
            <Link href="/habits" className="text-3xs text-primary hover:underline font-mono">MANAGE</Link>
          </div>

          <div className="space-y-2 text-xs">
            {loading ? (
              <p className="text-3xs text-muted-foreground italic">Auditing habits status...</p>
            ) : habits.length === 0 ? (
              <p className="text-3xs text-muted-foreground italic">No active habits logged.</p>
            ) : (
              habits.map((h) => {
                const todayStr = new Date().toISOString().split('T')[0];
                const checked = h.logs?.some((l) => l.date === todayStr);

                return (
                  <button
                    key={h.id}
                    onClick={() => toggleHabitLog(h)}
                    className="w-full flex items-center gap-3 p-2.5 rounded-xl border border-border bg-muted/20 text-left hover:border-primary/20 transition-all"
                  >
                    <CheckSquare className={`h-4.5 w-4.5 transition-colors ${checked ? 'text-primary' : 'text-muted-foreground'}`} />
                    <span className={`truncate font-medium ${checked ? 'line-through text-muted-foreground' : 'text-foreground'}`}>
                      {h.name}
                    </span>
                  </button>
                );
              })
            )}
          </div>
        </div>

        {/* Google Calendar schedule */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <div className="flex justify-between items-center pb-2 border-b border-border/40">
            <h2 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
              <CalendarIcon className="h-4 w-4 text-primary" />
              Schedule Timelines
            </h2>
            <Link href="/calendar" className="text-3xs text-primary hover:underline font-mono">SYNC</Link>
          </div>

          <div className="space-y-2.5 text-xs font-mono">
            {loading ? (
              <p className="text-3xs text-muted-foreground italic">Checking calendar schedules...</p>
            ) : todayEvents.length === 0 ? (
              <p className="text-3xs text-muted-foreground italic">No events scheduled today.</p>
            ) : (
              todayEvents.map((evt) => (
                <div key={evt.id} className="p-3 rounded-xl border border-border/60 bg-muted/25">
                  <span className="text-[10px] text-primary font-bold">
                    {new Date(evt.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                  <h4 className="font-semibold text-foreground mt-1 truncate">{evt.title}</h4>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Addiction recovery tracker streaks */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <div className="flex justify-between items-center pb-2 border-b border-border/40">
            <h2 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
              <Flame className="h-4 w-4 text-primary animate-pulse" />
              Recovery Streaks
            </h2>
            <Link href="/recovery" className="text-3xs text-primary hover:underline font-mono">MANAGE</Link>
          </div>

          <div className="space-y-3">
            {loading ? (
              <p className="text-3xs text-muted-foreground italic">Fetching recovery stats...</p>
            ) : addictions.length === 0 ? (
              <p className="text-3xs text-muted-foreground italic">No addiction tracks active.</p>
            ) : (
              addictions.map((add) => (
                <div key={add.id} className="p-3.5 rounded-xl border border-border/60 bg-muted/20 flex justify-between items-center text-xs font-semibold">
                  <div className="min-w-0">
                    <span className="block truncate">{add.name}</span>
                    <span className="text-3xs text-muted-foreground font-mono">
                      Saved: {currencySymbols[geo?.currency || 'USD'] || '$'}{add.money_saved || 0}
                    </span>
                  </div>
                  <span className="text-primary font-mono text-sm font-bold ml-2 shrink-0">{add.current_streak_days}d</span>
                </div>
              ))
            )}
          </div>
        </div>

        {/* AI Coach Assistant summary advice */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4 lg:col-span-2">
          <div className="flex justify-between items-center pb-2 border-b border-border/40">
            <h2 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
              <Brain className="h-4 w-4 text-primary" />
              AI Coach Insights
            </h2>
            <Link href="/ai-coach" className="text-3xs text-primary hover:underline font-mono">TALK TO COACH</Link>
          </div>

          {loading ? (
            <div className="py-4 text-center text-xs text-muted-foreground flex items-center gap-2">
              <Sparkles className="h-4.5 w-4.5 text-primary animate-spin" /> Auditing database summaries...
            </div>
          ) : insight ? (
            <p className="text-xs text-muted-foreground font-mono leading-relaxed bg-card/50 p-4 border border-border/60 rounded-xl">
              &quot;{insight.content}&quot;
            </p>
          ) : (
            <p className="text-xs text-muted-foreground">No coaching logs found.</p>
          )}
        </div>

        {/* Cloud storage provider health */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <h2 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2 pb-2 border-b border-border/40">
            <HardDrive className="h-4 w-4 text-primary" />
            Storage Health
          </h2>
          <div className="space-y-3">
            {loading ? (
              <p className="text-3xs text-muted-foreground italic">Loading active nodes...</p>
            ) : (
              providers.map((p, idx) => (
                <div key={idx} className="p-3 rounded-xl border border-border/60 bg-muted/20 space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-foreground">Drive {p.provider_label}</span>
                    <span className={`rounded-full px-2 py-0.5 text-3xs font-semibold ${
                      p.connected ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-muted text-muted-foreground border border-border'
                    }`}>
                      {p.connected ? 'ONLINE' : 'OFFLINE'}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
