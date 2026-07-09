'use client';

import React, { useEffect, useState } from 'react';

const TELEMETRY_ITEMS = [
  'SYSTEM AUDIT: OK',
  'BACKEND API: VERIFIED ONLINE',
  'PORTRAIT TRANSITIONS: PIXELATE SYNCED',
  'THEME PALETTE: ACCENT HSL DYNAMIC',
  'CORES: 8 ACTIVE ENGINE INSTANCES',
  'WSL TELEMETRY: 172.23.144.1 ROUTE OK',
  'DB CLUSTER: POSTGRESQL SECURE 12ms POOL',
  'GIT REVISION: c355916 RESOLVED',
  'MEM LEVEL: 94.2% ALLOCATED',
  'WI-FI GATEWAY: 192.168.1.5 PORT 3000',
  'PIPELINES: OPERATIONAL ON ALL SHELLS',
  'CLAUDE MCP CORE: ACTIVE AND LISTENING',
  'GEMINI RAG SCHEMA: SYNCED',
  'OPENAI FUNCTION STREAM: ROUTED',
];

export function SystemTelemetryTicker() {
  const [pulse, setPulse] = useState(true);

  // Blinking LED pulse simulator
  useEffect(() => {
    const interval = setInterval(() => {
      setPulse((prev) => !prev);
    }, 900);
    return () => clearInterval(interval);
  }, []);

  // Concatenate list twice to form a seamless infinite loop container
  const items = [...TELEMETRY_ITEMS, ...TELEMETRY_ITEMS];

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 h-7 border-t border-border/40 bg-background/70 backdrop-blur-md flex items-center justify-between select-none font-mono text-[9px] uppercase tracking-wider text-muted-foreground/80 overflow-hidden px-4">
      {/* Blinking LED Ticker Status Shield */}
      <div className="flex items-center gap-2 pr-3 border-r border-border/30 bg-background/50 h-full shrink-0 z-10">
        <span className="relative flex h-2 w-2">
          <span className={`animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75 ${pulse ? 'scale-110' : 'scale-50'}`}></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
        </span>
        <span className="font-pixel text-[8.5px] text-emerald-500/90 tracking-widest leading-none">
          AUDITING
        </span>
      </div>

      {/* Marquee Loop Container */}
      <div className="relative flex-1 overflow-hidden h-full flex items-center">
        <div className="animate-marquee flex items-center gap-12 cursor-default">
          {items.map((item, idx) => (
            <div key={idx} className="flex items-center gap-2 flex-shrink-0">
              <span className="text-primary/60">{"//"}</span>
              <span className="hover:text-primary transition-colors duration-200">{item}</span>
              <span className="w-1.5 h-1.5 rounded-full bg-border/40 mx-2 inline-block shrink-0" />
            </div>
          ))}
        </div>
      </div>

      {/* Telemetry Clock / Live Time */}
      <div className="pl-3 border-l border-border/30 bg-background/50 h-full flex items-center shrink-0 z-10 text-2xs text-muted-foreground/50 tracking-widest font-pixel font-bold gap-1.5">
        <span className="w-1 h-1 rounded-full bg-cyan-500 animate-pulse" />
        LIVE FEED
      </div>
    </div>
  );
}
