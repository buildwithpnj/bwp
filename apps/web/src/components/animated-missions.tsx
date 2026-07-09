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
    }, 40);
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
}

const missionSignals: MissionSignal[] = [
  {
    title: 'Production-First Deployment',
    description:
      'Engineering working software directly to production. Our pipelines favor operational execution over static engineering prototypes.',
    telemetry: 'SHIP MODE',
    Icon: Zap,
  },
  {
    title: 'Context-Aware Core',
    description:
      'Constructing stateful, vector-driven pipelines and memory retention models built for daily operational workflows.',
    telemetry: 'MEMORY ONLINE',
    Icon: Cpu,
  },
  {
    title: 'Open Architectures',
    description:
      'Publishing complete system designs, database schemas, and codebase blueprints for the developer community.',
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
    <div className="relative overflow-hidden rounded-2xl border border-border/40 bg-card/35 p-5 sm:p-6 backdrop-blur-md shadow-[0_12px_40px_rgba(0,0,0,0.03)]">
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
              <h3 key={signal.title} className="mt-1 text-base font-bold text-foreground animate-in">
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

        <p key={signal.description} className="max-w-xl text-sm leading-relaxed text-muted-foreground animate-in">
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
    const interval = window.setInterval(() => {
      setActiveIndex((current) => (current + 1) % missionSignals.length);
    }, 3600);

    return () => window.clearInterval(interval);
  }, []);

  return (
    <section className="grid grid-cols-1 items-center gap-8 lg:grid-cols-[minmax(0,1.05fr)_minmax(340px,0.95fr)]">
      <div className="flex max-w-3xl flex-col gap-3">
        <DecodedHeader text="// OPERATIONAL MISSION" />
        <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-foreground leading-tight">
          Architecting production-ready AI products, autonomous agent systems, and context-aware workspaces.
        </h2>
        <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
          We bypass theoretical delay to ship working software. Explore verified system architectures, database migration post-mortems, and active product blueprints.
        </p>
      </div>

      <MissionSignalCard signal={activeSignal} activeIndex={activeIndex} onSelect={setActiveIndex} />
    </section>
  );
}
