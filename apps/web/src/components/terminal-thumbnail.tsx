'use client';

import React, { useState, useEffect, useRef } from 'react';
import { cn } from '@/lib/utils';

interface TerminalThumbnailProps {
  index: number;
  slug?: string;
  mode?: 'projects' | 'journal' | 'labs';
}

interface SimState {
  lines: string[];
  progress: number;
  statusText: string;
  statusColor: string;
  metrics?: Record<string, string | number>;
}

interface Simulation {
  title: string;
  states: SimState[];
}

const SIMULATIONS: Record<string, Simulation> = {
  // Documentation CMS
  'monorepo-documentation-cms': {
    title: 'DOCS CMS PIPELINE',
    states: [
      {
        lines: [':> Scanning markdown directory...', 'Loading file nodes from workspace...', 'Target path: content/blog/*.md'],
        progress: 15,
        statusText: 'SCANNING',
        statusColor: 'text-amber-400',
        metrics: { FILES: 24, CACHE: 'MISS', SPEED: '---' }
      },
      {
        lines: ['[PARSER] Generating AST tree...', 'Extracting frontmatter variables...', 'Compiling routes index map...'],
        progress: 45,
        statusText: 'PARSING',
        statusColor: 'text-primary',
        metrics: { FILES: 24, AST: 'ACTIVE', SPEED: '12ms' }
      },
      {
        lines: ['[INDEX] Binding pgvector metadata...', 'Synchronizing tags & categories...', 'Building search queries index...'],
        progress: 75,
        statusText: 'INDEXING',
        statusColor: 'text-primary',
        metrics: { FILES: 24, VECTORS: 128, SPEED: '8ms' }
      },
      {
        lines: ['[COMPILER] Writing static HTML pages...', 'Optimizing Next.js image payloads...', 'Prerendering static output paths...'],
        progress: 92,
        statusText: 'COMPILING',
        statusColor: 'text-primary',
        metrics: { SIZE: '108kB', STATIC: 'YES', SPEED: '4ms' }
      },
      {
        lines: ['[DONE] Compilation completed cleanly.', 'Host routing: Vercel Edge Server active.', 'Static bundle optimized successfully.'],
        progress: 100,
        statusText: 'READY ●',
        statusColor: 'text-emerald-400',
        metrics: { DEPLOY: 'VERCEL', HEALTH: '100%', STATUS: 'OK' }
      }
    ]
  },
  // Voice AI / Model Router
  'cockroach-watch-india': {
    title: 'VOICE AI ROUTER',
    states: [
      {
        lines: ['[AUDIO] listening for verbal trigger...', 'Silent threshold set to 45db...', 'Active device: core_input_node'],
        progress: 10,
        statusText: 'LISTENING',
        statusColor: 'text-primary/70',
        metrics: { DB: 12, LATENCY: '---', CODEC: 'OPUS' }
      },
      {
        lines: ['[STT] Speech-to-text processing...', 'Client: "analyze recent comment feed"', 'Confidence match: 98.4%'],
        progress: 40,
        statusText: 'TRANSCRIBING',
        statusColor: 'text-amber-400',
        metrics: { LENGTH: '3.4s', PROCESS: 'STT', CODEC: 'OPUS' }
      },
      {
        lines: ['[AGENT] Neural reasoning active...', 'Context buffer: 1,480 tokens.', 'Model selection: Claude-3-Sonnet'],
        progress: 70,
        statusText: 'AI THINKING',
        statusColor: 'text-primary',
        metrics: { MODEL: 'CLAUDE', TOKENS: 1480, TEMP: 0.2 }
      },
      {
        lines: ['[TTS] Synthesizing speech stream...', 'Streaming audio buffer chunks...', 'Latency rate: 124ms (low-latency)'],
        progress: 90,
        statusText: 'STREAMING',
        statusColor: 'text-primary',
        metrics: { CHUNKS: 24, DELAY: '124ms', AUDIO: 'PCM' }
      },
      {
        lines: ['[COMPLETE] Outbound voice transaction done.', 'Usage: 382 prompt, 120 completion.', 'Pipeline returned to sleep mode.'],
        progress: 100,
        statusText: 'COMPLETED ●',
        statusColor: 'text-emerald-400',
        metrics: { USAGE: '0.01$', SESSION: 'DONE', HEARTH: 'OK' }
      }
    ]
  },
  // MCP Code Analyzer
  'agentix-code-analyzer': {
    title: 'MCP DOCUMENT AUDIT',
    states: [
      {
        lines: ['[MCP] Establishing client bridge...', 'Target: localhost:8080/mcp/v1', 'Querying capabilities schema...'],
        progress: 15,
        statusText: 'CONNECTING',
        statusColor: 'text-amber-400',
        metrics: { PING: '14ms', PORT: 8080, PROTO: 'JSON-RPC' }
      },
      {
        lines: ['[TOOLS] Registering workspace methods...', 'Loaded: inspect_file, list_dir, grep_search', 'Sandbox container: ACTIVE (Docker)'],
        progress: 45,
        statusText: 'INGESTING',
        statusColor: 'text-primary',
        metrics: { TOOLS: 8, SANDBOX: 'SECURE', PROTO: 'JSON-RPC' }
      },
      {
        lines: ['[CONTEXT] Syncing codebase index...', 'Ingesting 16 repository configurations...', 'Vector embeddings chunking active...'],
        progress: 75,
        statusText: 'SYNCING',
        statusColor: 'text-primary',
        metrics: { REPOS: 16, INDEX: 'FAISS', SPEED: '1.2s' }
      },
      {
        lines: ['[AUDIT] Analyzing code dependencies...', 'Running dependency security scanner...', 'Resolving import symbol references...'],
        progress: 90,
        statusText: 'AUDITING',
        statusColor: 'text-primary',
        metrics: { FILES: 482, ERRORS: 0, WARNS: 0 }
      },
      {
        lines: ['[DONE] Workspace audit completed.', 'Vulnerabilities: 0 warning, 0 error.', 'Diagnostic log saved to file ledger.'],
        progress: 100,
        statusText: 'SECURE ●',
        statusColor: 'text-emerald-400',
        metrics: { STATUS: 'OK', LEAKS: 0, THREAT: '0%' }
      }
    ]
  },
  // Personal OS
  'personal-os': {
    title: 'WARBORN OS SUBSYSTEM',
    states: [
      {
        lines: ['[BOOT] Initializing Warborn core...', 'Loading note files, habits catalog...', 'Checking workspace dependencies...'],
        progress: 20,
        statusText: 'BOOTING',
        statusColor: 'text-amber-400',
        metrics: { CORE: 'ACTIVE', UPTIME: '1s', BOOT: 'OK' }
      },
      {
        lines: ['[SYNC] Linking storage credentials...', 'Fetching Google Drive API credentials...', 'Sync callback token verified.'],
        progress: 50,
        statusText: 'SYNCING GDRIVE',
        statusColor: 'text-primary',
        metrics: { GDRIVE: 'AUTH', CACHE: 'SYNCED', BOOT: 'OK' }
      },
      {
        lines: ['[DB] Resolving Postgres connections...', 'Applying Alembic schema upgrades...', 'Supabase pool host connected.'],
        progress: 75,
        statusText: 'DB UPDATE',
        statusColor: 'text-primary',
        metrics: { DB: 'SUPABASE', POOL: 10, SCHEMA: 'HEAD' }
      },
      {
        lines: ['[CELERY] Starting background worker...', 'Broker: Upstash Redis secure caching', 'Active worker queue listening...'],
        progress: 90,
        statusText: 'CELERY UP',
        statusColor: 'text-primary',
        metrics: { CELERY: 'RUN', QUEUES: 3, BROKER: 'UPSTASH' }
      },
      {
        lines: ['[SYSTEM] OS online & telemetry syncing.', 'Active prompts allocated in memory.', 'Core health: 100% (Nominal)'],
        progress: 100,
        statusText: 'ONLINE ●',
        statusColor: 'text-emerald-400',
        metrics: { CPU: '24%', MEM: '61%', AGENTS: 94 }
      }
    ]
  },
  // PricePilot / Automation
  'pricepilot': {
    title: 'AUTOMATION PIPELINE',
    states: [
      {
        lines: ['[TRIGGER] Cron job scheduler fired...', 'Job identifier: compare_retailer_prices', 'Queue state: listening (priority)'],
        progress: 20,
        statusText: 'TRIGGERED',
        statusColor: 'text-amber-400',
        metrics: { JOB: 'COMPARE', RUNS: 482, ERRORS: 0 }
      },
      {
        lines: ['[CRAWLER] Rotated proxy pool mapping...', 'Targeting e-commerce inventory catalogs...', 'Resolving dynamic browser headers...'],
        progress: 50,
        statusText: 'CRAWLING',
        statusColor: 'text-primary',
        metrics: { PROXIES: 8, RETRIES: 0, SPEED: '3.2s' }
      },
      {
        lines: ['[VALIDATOR] Bypassing cloudflare limits...', 'Cookies extracted. Parsing payload JSON...', 'Matched target price thresholds.'],
        progress: 75,
        statusText: 'VALIDATING',
        statusColor: 'text-primary',
        metrics: { ITEMS: 480, PARSED: 480, BOT: 'BYPASS' }
      },
      {
        lines: ['[DEPLOYMENT] Pushing inventory metrics...', 'Syncing database schema price history...', 'Triggering Slack messaging callbacks...'],
        progress: 90,
        statusText: 'DEPLOYING',
        statusColor: 'text-primary',
        metrics: { SLACK: 'OK', DB: 'UPDATED', PUSH: 'YES' }
      },
      {
        lines: ['[DONE] Price comparison job complete.', 'Execution time: 4.8 seconds.', 'Next scheduler run in 1 hour.'],
        progress: 100,
        statusText: 'SLEEP ●',
        statusColor: 'text-emerald-400',
        metrics: { STATUS: 'OK', TIME: '4.8s', COOLDOWN: '3600s' }
      }
    ]
  }
};

// Default generic templates for other project indexes
const GENERIC_SIMULATIONS: Simulation[] = [
  // Generic 0: Design Lab / UI showcase
  {
    title: 'DESIGN LAB ENGINE',
    states: [
      {
        lines: [':> Parsing layout components...', 'Loading CSS custom property variables...', 'Binding Framer Motion springs...'],
        progress: 20,
        statusText: 'PARSING',
        statusColor: 'text-amber-400',
        metrics: { NODES: 12, SPRING: 'OFF', FPS: '---' }
      },
      {
        lines: ['[GLOW] Compiling dynamic backdrop filters...', 'Initializing hardware-accelerated shaders...', 'Prerendering glass overlays...'],
        progress: 60,
        statusText: 'RENDER BOOT',
        statusColor: 'text-primary',
        metrics: { SHADERS: 4, GLOW: 'ACTIVE', FPS: '60' }
      },
      {
        lines: ['[OPTIMIZER] Compiling layout variables...', 'Testing hardware scroll frame drops...', 'Bypassing CPU thread latency...'],
        progress: 90,
        statusText: 'OPTIMIZING',
        statusColor: 'text-primary',
        metrics: { CPU: '2%', GPU: 'ACTIVE', FPS: '60' }
      },
      {
        lines: ['[SYSTEM] Interface layout is fully synced.', 'Dynamic color bindings synced successfully.', 'Status: Nominal (60 FPS locked)'],
        progress: 100,
        statusText: 'STABLE ●',
        statusColor: 'text-emerald-400',
        metrics: { SCALE: 1.0, GLOW: 'YES', FPS: '60' }
      }
    ]
  },
  // Generic 1: Energy / Resource optimization
  {
    title: 'RESOURCE ANALYZER',
    states: [
      {
        lines: [':> Establishing API database socket...', 'Querying smart meters telemetry...', 'Collecting historical energy data...'],
        progress: 15,
        statusText: 'BOOTING',
        statusColor: 'text-amber-400',
        metrics: { METERS: 124, LOSS: '---', PING: '18ms' }
      },
      {
        lines: ['[COMPUTE] Running linear resource regression...', 'Weighting resource constraint metrics...', 'Locating utility pool leaks...'],
        progress: 55,
        statusText: 'COMPUTING',
        statusColor: 'text-primary',
        metrics: { METERS: 124, WEIGHTS: 'SYNC', PING: '12ms' }
      },
      {
        lines: ['[SAVINGS] Adjusting utility grid limits...', 'Syncing local node load balancing...', 'Registering peak usage cutoffs...'],
        progress: 85,
        statusText: 'BALANCING',
        statusColor: 'text-primary',
        metrics: { METERS: 124, REDUX: '14%', LEAKS: 0 }
      },
      {
        lines: ['[DONE] Resource savings locked.', 'Energy efficiency raised: 14.8%', 'Telemetry logs synced successfully.'],
        progress: 100,
        statusText: 'OPTIMAL ●',
        statusColor: 'text-emerald-400',
        metrics: { REDUX: '14.8%', HEALTH: '100%', SYS: 'OK' }
      }
    ]
  },
  // Generic 2: Generic pipeline builder
  {
    title: 'TASK DISPATCHER',
    states: [
      {
        lines: [':> Reading task queue entries...', 'Found 8 uncompleted tasks in line...', 'Initializing processing pool...'],
        progress: 25,
        statusText: 'QUEUED',
        statusColor: 'text-amber-400',
        metrics: { TASKS: 8, WORKERS: 0, PING: '---' }
      },
      {
        lines: ['[DISPATCH] Mounting task routines...', 'Executing worker callback instances...', 'Updating tasks status ledger...'],
        progress: 65,
        statusText: 'PROCESSING',
        statusColor: 'text-primary',
        metrics: { TASKS: 4, WORKERS: 4, PING: '14ms' }
      },
      {
        lines: ['[SUCCESS] Worker threads finished cleanly.', 'All queues return to standby status.', 'Diagnostic report saved to storage.'],
        progress: 100,
        statusText: 'IDLE ●',
        statusColor: 'text-emerald-400',
        metrics: { TASKS: 0, WORKERS: 0, PING: '12ms' }
      }
    ]
  }
];

export function TerminalThumbnail({ index, slug = '', mode = 'projects' }: TerminalThumbnailProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [activeState, setActiveState] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [paused, setPaused] = useState(false);
  const [prefersReduced, setPrefersReduced] = useState(false);

  // Determine active simulation
  let sim: Simulation;
  
  if (mode === 'journal') {
    sim = {
      title: 'JOURNAL STATIC BUILDER',
      states: [
        {
          lines: [':> Parsing post MD...', 'Extracting frontmatter data...', 'Calculating reading time...'],
          progress: 30,
          statusText: 'PARSING',
          statusColor: 'text-amber-400',
          metrics: { WORDS: 1482, AST: 'OK', READ: '6m' }
        },
        {
          lines: ['[INDEX] Generating search index mappings...', 'Translating tags to FAISS vectors...', 'Context payload: 1,480 tokens'],
          progress: 70,
          statusText: 'INDEXING',
          statusColor: 'text-primary',
          metrics: { WORDS: 1482, VECTORS: 128, READ: '6m' }
        },
        {
          lines: ['[SYSTEM] Static synced successfully.', 'Host routing: Vercel CDN Edge Server active.', 'All routes compiled and ready.'],
          progress: 100,
          statusText: 'ONLINE ●',
          statusColor: 'text-emerald-400',
          metrics: { INTEGRITY: 'VALID', DEPLOY: 'OK', STAT: 'READY' }
        }
      ]
    };
  } else if (mode === 'labs') {
    sim = {
      title: 'LAB SIMULATION RUNNER',
      states: [
        {
          lines: [':> Tokenizing target prompt context...', 'MODEL: Llama-3-70B instruction tuning', 'Active parameters loaded into cache...'],
          progress: 25,
          statusText: 'TOKENIZING',
          statusColor: 'text-amber-400',
          metrics: { MODEL: 'LLAMA', TOKENS: 2048, FPS: '---' }
        },
        {
          lines: ['[RUN] Compiling training optimizer...', 'Learning rate: 0.0003 | ADAM solver', 'Running neural weight gradients...'],
          progress: 60,
          statusText: 'OPTIMIZING',
          statusColor: 'text-primary',
          metrics: { LOSS: '0.084', TEMP: 0.2, FPS: '60' }
        },
        {
          lines: ['[SYSTEM] Neural simulation completed.', 'Success rate: 98.4% (Stable)', 'Diagnostic reports ingested successfully.'],
          progress: 100,
          statusText: 'STABLE ●',
          statusColor: 'text-emerald-400',
          metrics: { LOSS: '0.018', ACC: '98.4%', SYS: 'OK' }
        }
      ]
    };
  } else {
    // Projects mode: Select simulation by slug, fallback to index
    if (slug && SIMULATIONS[slug]) {
      sim = SIMULATIONS[slug];
    } else {
      sim = GENERIC_SIMULATIONS[index % GENERIC_SIMULATIONS.length];
    }
  }

  const totalStates = sim.states.length;
  const currentState = sim.states[activeState] || sim.states[0];

  // 1. Detect prefers-reduced-motion
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const media = window.matchMedia('(prefers-reduced-motion: reduce)');
      setPrefersReduced(media.matches);
      const listener = (e: MediaQueryListEvent) => setPrefersReduced(e.matches);
      media.addEventListener('change', listener);
      return () => media.removeEventListener('change', listener);
    }
  }, []);

  // 2. Automate transitions every 5 seconds (paused on hover, staggered start)
  useEffect(() => {
    if (paused) return;

    let interval: NodeJS.Timeout;
    
    // Stagger start based on card index (index * 1200ms delay)
    const delayMs = index * 1200;
    
    const startTimeout = setTimeout(() => {
      interval = setInterval(() => {
        setIsTransitioning(true);
        
        setTimeout(() => {
          setActiveState((prev) => (prev + 1) % totalStates);
          setIsTransitioning(false);
        }, 250); // Match fade duration
      }, 5000);
    }, delayMs);

    return () => {
      clearTimeout(startTimeout);
      if (interval) clearInterval(interval);
    };
  }, [paused, totalStates, index]);

  // 3. Attach hover event listeners to closest parent anchor tag
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const parentCard = el.closest('a');
    if (!parentCard) return;

    const handleEnter = () => {
      setPaused(true);
      // Resolve sync color for this thumbnail card and dispatch global event
      let targetColor: 'blue' | 'red' | 'muted' = 'blue';
      if (mode === 'labs') {
        const colors: ('blue' | 'red' | 'muted')[] = ['blue', 'red', 'muted'];
        targetColor = colors[index % 3];
      } else if (mode === 'projects') {
        const colors: ('blue' | 'red' | 'muted')[] = ['red', 'muted', 'blue'];
        targetColor = colors[index % 3];
      } else {
        const colors: ('blue' | 'red' | 'muted')[] = ['muted', 'blue', 'red'];
        targetColor = colors[index % 3];
      }
      window.dispatchEvent(new CustomEvent('pnj-sync-color', { detail: { key: targetColor } }));
    };
    
    const handleLeave = () => {
      setPaused(false);
      window.dispatchEvent(new CustomEvent('pnj-sync-color', { detail: { key: null } }));
    };

    parentCard.addEventListener('mouseenter', handleEnter);
    parentCard.addEventListener('mouseleave', handleLeave);

    return () => {
      parentCard.removeEventListener('mouseenter', handleEnter);
      parentCard.removeEventListener('mouseleave', handleLeave);
    };
  }, [index, mode]);

  return (
    <div 
      ref={containerRef}
      className="w-full h-full p-3 sm:p-4 bg-background/95 flex flex-col justify-between select-none relative text-left border border-border/10 overflow-hidden rounded-lg"
    >
      {/* 1. Header Bar */}
      <div className={cn(
        "flex items-center justify-between border-b border-border/20 pb-1.5 shrink-0",
        mode === 'projects' && "pr-24" // Leave space for overlaid status/category badges on the top right
      )}>
        <span className="font-mono text-[8px] font-bold tracking-widest text-muted-foreground uppercase leading-none truncate max-w-[50%]">
          {`// ${sim.title}`}
        </span>
        <span className={cn(
          "font-mono text-[8px] font-bold uppercase tracking-wider flex items-center gap-1 leading-none transition-colors duration-300",
          currentState.statusColor
        )}>
          {currentState.statusText}
          {currentState.statusText.includes('●') ? null : (
            <span className="h-1.5 w-1.5 rounded-full bg-current animate-pulse shrink-0" />
          )}
        </span>
      </div>

      {/* 2. Terminal Body (Animated Terminal Screen Lines) */}
      <div className={cn(
        "flex-1 flex flex-col justify-center gap-1 font-mono text-[9px] sm:text-[10px] leading-relaxed text-primary transition-all duration-300 ease-out py-2.5",
        prefersReduced 
          ? (isTransitioning ? "opacity-0" : "opacity-100")
          : (isTransitioning ? "opacity-0 translate-y-1 blur-[1px] scale-[0.98]" : "opacity-100 translate-y-0 blur-0 scale-100")
      )}>
        {currentState.lines.map((line, idx) => {
          const isLastLine = idx === currentState.lines.length - 1;
          return (
            <div key={idx} className="truncate flex items-center gap-0.5 min-h-[14px]">
              <span className="opacity-90">{line}</span>
              {isLastLine && !isTransitioning && (
                <span className="inline-block w-1 h-3 bg-primary animate-caret-blink shrink-0" />
              )}
            </div>
          );
        })}
      </div>

      {/* 3. Footer Bar: Live Progress Meter & Hardware Telemetry Grid */}
      <div className="flex flex-col gap-1.5 shrink-0 pt-1.5 border-t border-border/20">
        {/* Flat Progress Loader Fill Track */}
        <div className="h-1.5 w-full bg-secondary/60 rounded-full overflow-hidden border border-border/15 relative z-10">
          <div 
            className="h-full bg-primary rounded-full transition-all duration-1000 ease-out"
            style={{ width: `${currentState.progress}%` }}
          />
        </div>

        {/* Telemetry Metrics Grid */}
        {currentState.metrics && (
          <div className="grid grid-cols-3 gap-1 text-[8px] font-mono text-muted-foreground leading-none">
            {Object.entries(currentState.metrics).map(([key, val]) => (
              <div key={key} className="flex justify-between items-center bg-secondary/20 px-1 py-0.5 rounded border border-border/10">
                <span className="opacity-70">{key}</span>
                <span className="font-bold text-foreground truncate pl-0.5">{val}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
