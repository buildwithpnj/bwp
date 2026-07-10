'use client';

import React, { useEffect, useState } from 'react';
import { Cpu, Radio, Zap } from 'lucide-react';

function DecodedHeader({ text }: { text: string }) {
  const [display, setDisplay] = useState('');

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      setDisplay(text.substring(0, index));
      index++;
      if (index > text.length) {
        clearInterval(interval);
      }
    }, 45);
    return () => clearInterval(interval);
  }, [text]);

  return (
    <span className="font-mono text-[10px] tracking-[0.25em] text-primary/80 uppercase min-h-[15px] block">
      {display}
      <span className="animate-pulse">_</span>
    </span>
  );
}

interface MissionSignal {
  title: string;
  description: string;
  telemetry: string;
  Icon: typeof Zap;
  // Left-Side dynamic main screen copy
  header: string;
  heading: string;
  mainDesc: string;
}

const missionSignals: MissionSignal[] = [
  {
    header: '// OPERATIONAL MISSION',
    heading: 'Architecting production-ready AI products, autonomous agent systems, and context-aware workspaces.',
    mainDesc: 'We bypass theoretical delay to ship working software. Explore verified system architectures, database migration post-mortems, and active product blueprints.',
    title: 'Production-First Deployment',
    description: 'Engineering working software directly to production. Our pipelines favor operational execution over static engineering prototypes.',
    telemetry: 'SHIP MODE',
    Icon: Zap,
  },
  {
    header: '// INFRASTRUCTURE ORCHESTRATION',
    heading: 'Building multi-agent task execution grids, persistent vector graphs, and low-latency API routers.',
    mainDesc: 'Deploying scalable memory contexts and event-driven LLM orchestration. Analyze production trace runs, real-time token performance, and system throughput.',
    title: 'Context-Aware Core',
    description: 'Constructing stateful, vector-driven pipelines and memory retention models built for daily operational workflows.',
    telemetry: 'MEMORY ONLINE',
    Icon: Cpu,
  },
  {
    header: '// SEMANTIC DATA PIPELINES',
    heading: 'Deploying self-correcting RAG systems, knowledge synthesis layers, and context extraction blocks.',
    mainDesc: 'Bridging the gap between unstructured storage and agentic recall. Inspect vector space search parameters, memory caching loops, and model convergence profiles.',
    title: 'Open Architectures',
    description: 'Publishing complete system designs, database schemas, and codebase blueprints for the developer community.',
    telemetry: 'SCHEMA OPEN',
    Icon: Radio,
  },
];

function MissionSignalCard({
  signal,
  activeIndex,
  onSelect,
}: {
  signal: MissionSignal;
  activeIndex: number;
  onSelect: (index: number) => void;
}) {
  const Icon = signal.Icon;

  return (
    <div className="relative overflow-hidden rounded-2xl border border-border/40 bg-background/95 dark:bg-card/95 p-5 sm:p-6 backdrop-blur-xl shadow-[0_12px_36px_rgba(0,0,0,0.1)] dark:shadow-[0_12px_36px_rgba(0,0,0,0.45)] hover:-translate-y-1.5 hover:border-primary/40 hover:shadow-[0_20px_48px_rgba(0,0,0,0.15)] dark:hover:shadow-[0_20px_48px_rgba(0,0,0,0.55)] transition-all duration-300">
      <div className="absolute -right-16 -top-20 h-48 w-48 rounded-full bg-primary/10 blur-[70px]" />
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-primary/45 to-transparent" />

      <div className="relative flex min-h-[188px] flex-col justify-between gap-5">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-primary/15 bg-primary/10">
              <Icon className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-primary/80">
                {signal.telemetry}
              </p>
              <h3 key={signal.title} className="mt-1 text-base font-bold text-foreground animate-in fade-in slide-in-from-bottom-1 duration-500">
                {signal.title}
              </h3>
            </div>
          </div>

          <div className="hidden h-10 items-center gap-1 rounded-full border border-border/40 bg-background/40 px-2 sm:flex">
            {missionSignals.map((item, index) => (
              <button
                key={item.title}
                type="button"
                aria-label={`Show ${item.title}`}
                onClick={() => onSelect(index)}
                className={`h-2 rounded-full transition-all ${
                  index === activeIndex ? 'w-6 bg-primary' : 'w-2 bg-muted-foreground/30 hover:bg-muted-foreground/60'
                }`}
              />
            ))}
          </div>
        </div>

        <p key={signal.description} className="max-w-xl text-sm leading-relaxed text-muted-foreground animate-in fade-in slide-in-from-bottom-1 duration-500">
          {signal.description}
        </p>

        <div className="grid grid-cols-3 gap-2 border-t border-border/30 pt-4">
          {missionSignals.map((item, index) => {
            const ItemIcon = item.Icon;
            const isActive = index === activeIndex;

            return (
              <button
                key={item.title}
                type="button"
                onClick={() => onSelect(index)}
                className={`flex h-10 items-center justify-center rounded-lg border transition-all ${
                  isActive
                    ? 'border-primary/30 bg-primary/10 text-primary'
                    : 'border-border/35 bg-secondary/40 text-muted-foreground hover:border-primary/20 hover:text-foreground'
                }`}
                aria-pressed={isActive}
              >
                <ItemIcon className="h-4 w-4" />
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}

/* ============================================================================
   MAIN COMPONENT: AnimatedMissions
   ============================================================================ */
export function AnimatedMissions() {
  const [activeIndex, setActiveIndex] = useState(0);
  const activeSignal = missionSignals[activeIndex];

  useEffect(() => {
    const colors: ('red' | 'blue' | 'muted')[] = ['red', 'blue', 'muted'];
    const activeColor = colors[activeIndex % colors.length];
    window.dispatchEvent(new CustomEvent('pnj-sync-color', { detail: { key: activeColor } }));
  }, [activeIndex]);

  useEffect(() => {
    const interval = window.setInterval(() => {
      setActiveIndex((current) => (current + 1) % missionSignals.length);
    }, 4500); // 4.5 seconds for comfortable reading

    return () => window.clearInterval(interval);
  }, [activeIndex]);

  return (
    <section className="grid grid-cols-1 items-center gap-8 lg:grid-cols-[minmax(0,1fr)_minmax(420px,1fr)]">
      <div className="flex max-w-3xl flex-col gap-3">
        <DecodedHeader key={activeSignal.header} text={activeSignal.header} />
        
        <h2 
          key={activeSignal.heading} 
          className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-foreground leading-tight animate-in fade-in slide-in-from-bottom-2 duration-700"
        >
          {activeSignal.heading}
        </h2>
        
        <p 
          key={activeSignal.mainDesc} 
          className="text-sm sm:text-base text-muted-foreground leading-relaxed animate-in fade-in slide-in-from-bottom-2 duration-900"
        >
          {activeSignal.mainDesc}
        </p>
      </div>

      <MissionSignalCard signal={activeSignal} activeIndex={activeIndex} onSelect={setActiveIndex} />
    </section>
  );
}
