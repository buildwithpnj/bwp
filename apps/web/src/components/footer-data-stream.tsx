'use client';

import React, { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// ─── Engineering Node Definition ─────────────────────────────────────────────
interface DataNode {
  id: string;
  label: string;
  x: number;
  y: number;
  desc: string;
}

const NODES: DataNode[] = [
  { id: 'api', label: 'API', x: 120, y: 30, desc: 'REST & gRPC Integration Endpoints' },
  { id: 'llm', label: 'LLM', x: 240, y: 30, desc: 'Large Language Model Router & Cost Optimization' },
  { id: 'rag', label: 'RAG', x: 340, y: 55, desc: 'Retrieval-Augmented Generation context pipeline' },
  { id: 'json', label: 'JSON', x: 440, y: 80, desc: 'Structured schema serialization layers' },
  { id: 'sql', label: 'SQL', x: 550, y: 80, desc: 'Relational transaction databases & query planners' },
  { id: 'cache', label: 'CACHE', x: 640, y: 55, desc: 'Redis cache synchronization layer' },
  { id: 'gpu', label: 'GPU', x: 740, y: 30, desc: 'Hardware inference acceleration cluster' },
  { id: 'cpu', label: 'CPU', x: 860, y: 30, desc: 'Task orchestrator & CPU scheduling grid' },
  { id: 'tools', label: 'TOOLS', x: 960, y: 55, desc: 'Dynamic agentic tools execution framework' },
  { id: 'voice', label: 'VOICE', x: 1060, y: 80, desc: 'Low-latency Realtime multilingual voice pipelines' },
  { id: 'mcp', label: 'MCP', x: 1130, y: 55, desc: 'Model Context Protocol server integrations' },
  { id: 'node', label: 'NODE', x: 1010, y: 105, desc: 'Distributed microservice runtime nodes' },
  { id: 'token', label: 'TOKEN', x: 890, y: 105, desc: 'Context token streaming & rate limiting' },
  { id: 'vector', label: 'VECTOR', x: 720, y: 105, desc: 'Vector database similarity indexing' },
  { id: 'memory', label: 'MEMORY', x: 500, y: 105, desc: 'Persistent chat state & episodic memory structures' },
  { id: 'embedding', label: 'EMBEDDING', x: 200, y: 105, desc: 'High-dimensional text representation model' }
];

// Continuous path passing through all nodes
// Drawn with rounded corners (using Q & S bezier commands) for smooth travel
const CIRCUIT_PATH = `
  M 60,30 
  L 230,30 
  Q 240,30 250,35
  L 330,50
  Q 340,55 350,60
  L 430,80
  Q 440,80 450,80
  L 540,80
  Q 550,80 560,75
  L 630,60
  Q 640,55 650,50
  L 730,30
  Q 740,30 750,30
  L 850,30
  Q 860,30 870,35
  L 950,50
  Q 960,55 970,60
  L 1050,80
  Q 1060,80 1070,75
  L 1120,60
  Q 1130,55 1140,65
  L 1140,95
  Q 1140,105 1130,105
  L 1000,105
  Q 990,105 980,105
  L 880,105
  Q 870,105 860,105
  L 710,105
  Q 700,105 690,105
  L 490,105
  Q 480,105 470,105
  L 190,105
  Q 180,105 170,100
  L 60,70
  Q 50,65 50,55
  L 50,35
  Q 50,30 60,30
  Z
`.replace(/\s+/g, ' ').trim();

  // Status updates matching packet discovery
  const statusLabels = [
    'SYSTEM ONLINE',
    'MEMORY ACTIVE',
    'TOOLS READY',
    'VOICE READY',
    'RAG INDEXED',
    'MODELS LOADED',
    'PIPELINES NOMINAL',
    'VECTOR CACHE SYNCD'
  ];

export function FooterDataStream() {
  const containerRef = useRef<HTMLDivElement>(null);
  const pathRef = useRef<SVGPathElement>(null);
  
  const [collected, setCollected] = useState<Record<string, boolean>>({});
  const [activeNode, setActiveNode] = useState<DataNode | null>(null);
  const [pulseNode, setPulseNode] = useState<string | null>(null);
  const [statusText, setStatusText] = useState('SYSTEM ONLINE');
  const [showSyncMessage, setShowSyncMessage] = useState(false);
  const [trailLength, setTrailLength] = useState(6);
  const [inViewport, setInViewport] = useState(false);

  // States to animate the packet trail using react refs for 60fps performance
  const packetRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  const trailRef = useRef<{ x: number; y: number }[]>([]);
  const animationRef = useRef<number | null>(null);
  const progressRef = useRef(0);


  // Intersection Observer to pause animation offscreen
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        setInViewport(entry.isIntersecting);
      },
      { threshold: 0.1 }
    );

    if (containerRef.current) {
      observer.observe(containerRef.current);
    }

    return () => observer.disconnect();
  }, []);

  // Main animation loop
  useEffect(() => {
    if (!inViewport) {
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
      return;
    }

    // Prefers-reduced-motion check
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;

    const path = pathRef.current;
    if (!path) return;

    const totalLength = path.getTotalLength();
    let lastTime = 0;
    
    // Scale speed to feel elegant and premium
    const speed = 1.6;

    const animate = (time: number) => {
      // Limit speed or check if initialized
      if (!lastTime) lastTime = time;

      progressRef.current = (progressRef.current + speed) % totalLength;
      
      const headPoint = path.getPointAtLength(progressRef.current);
      packetRef.current = { x: headPoint.x, y: headPoint.y };

      // Update trail array
      trailRef.current.push({ x: headPoint.x, y: headPoint.y });
      if (trailRef.current.length > trailLength) {
        trailRef.current.shift();
      }

      // Render the trail packet elements
      const dots = document.querySelectorAll('.data-packet-trail');
      dots.forEach((dot, index) => {
        const trailIndex = Math.max(0, trailRef.current.length - 1 - index);
        const point = trailRef.current[trailIndex];
        if (point && dot) {
          (dot as HTMLElement).style.transform = `translate3d(${point.x}px, ${point.y}px, 0)`;
        }
      });

      // Update head packet element
      const head = document.getElementById('data-packet-head');
      if (head) {
        head.style.transform = `translate3d(${headPoint.x}px, ${headPoint.y}px, 0)`;
      }

      // Check collision with nodes
      NODES.forEach((node) => {
        const dx = headPoint.x - node.x;
        const dy = headPoint.y - node.y;
        const distSq = dx * dx + dy * dy;

        // Within 14 pixels triggers discovery
        if (distSq < 196 && !collected[node.id]) {
          setCollected((prev) => {
            const next = { ...prev, [node.id]: true };
            
            // Check if all collected
            const allCollected = NODES.every((n) => next[n.id]);
            if (allCollected) {
              setShowSyncMessage(true);
              setStatusText('COMPILING KNOWLEDGE...');
              setTimeout(() => {
                setShowSyncMessage(false);
                setCollected({});
                setTrailLength(6);
                setStatusText('SYSTEM ONLINE');
              }, 3000);
            }
            return next;
          });

          // Pulse trigger
          setPulseNode(node.id);
          setTimeout(() => setPulseNode(null), 400);

          // Grow trail
          setTrailLength((prev) => Math.min(prev + 1, 30));

          // Cycle status text
          setStatusText(statusLabels[Math.floor(Math.random() * statusLabels.length)]);
        }
      });

      animationRef.current = requestAnimationFrame(animate);
    };

    animationRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
    };
  }, [inViewport, collected, trailLength]);

  return (
    <div 
      ref={containerRef}
      className="w-full relative border border-border/40 rounded-xl bg-card/10 backdrop-blur-md overflow-hidden py-6 select-none"
    >
      {/* Schematic Layout micro details grid background */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(148,163,184,0.03)_1px,transparent_1px),linear-gradient(to_bottom,rgba(148,163,184,0.03)_1px,transparent_1px)] bg-[size:24px_24px] pointer-events-none" />

      {/* Engineering Info Bar */}
      <div className="flex items-center justify-between px-6 pb-4 border-b border-border/20 font-mono text-[9px] text-muted-foreground/80">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5">
            <span className="h-1.5 w-1.5 rounded-full bg-primary animate-pulse" />
            AI NETWORK: ONLINE
          </span>
          <span className="hidden sm:inline">RATE: 1.6MBPS</span>
          <span className="hidden md:inline">COMPILATION: PNJ-SYS.INFRA</span>
        </div>
        <div className="text-primary font-semibold tracking-wider">
          STATUS: {statusText}
        </div>
      </div>

      {/* Central Visualizer Area */}
      <div className="relative w-full h-[140px] mt-2 overflow-x-auto overflow-y-hidden scrollbar-none flex justify-center items-center">
        <div className="min-w-[1200px] w-[1200px] h-[140px] relative shrink-0">
          
          <svg className="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 1200 140">
            {/* Background Circuit Path */}
            <path
              ref={pathRef}
              d={CIRCUIT_PATH}
              fill="none"
              stroke="currentColor"
              className="text-border/40 dark:text-border/10"
              strokeWidth="1.5"
              strokeDasharray="4 4"
            />

            {/* Glowing Flow trace underlying the path */}
            <path
              d={CIRCUIT_PATH}
              fill="none"
              stroke="var(--primary)"
              className="opacity-[0.08]"
              strokeWidth="3.5"
            />
          </svg>

          {/* Glowing Head Packet (Square) */}
          <div
            id="data-packet-head"
            className="absolute top-0 left-0 w-[8px] h-[8px] bg-primary shadow-[0_0_8px_var(--primary)] rounded-sm pointer-events-none z-10"
            style={{ margin: '-4px 0 0 -4px' }}
          />

          {/* Trail Packet Pixels */}
          {Array.from({ length: 30 }).map((_, i) => (
            <div
              key={i}
              className="data-packet-trail absolute top-0 left-0 w-[5px] h-[5px] bg-primary/60 rounded-sm pointer-events-none"
              style={{
                margin: '-2.5px 0 0 -2.5px',
                opacity: Math.max(0.05, 0.7 - i * 0.05),
                transform: 'scale(' + Math.max(0.4, 1 - i * 0.04) + ')'
              }}
            />
          ))}

          {/* Interactive Engineering Objects (Nodes) */}
          {NODES.map((node) => {
            const isCollected = collected[node.id];
            const isHovered = activeNode?.id === node.id;
            const isPulsing = pulseNode === node.id;

            return (
              <div
                key={node.id}
                className="absolute font-mono text-[9px] group cursor-pointer"
                style={{
                  left: node.x,
                  top: node.y,
                  transform: 'translate(-50%, -50%)',
                }}
                onMouseEnter={() => setActiveNode(node)}
                onMouseLeave={() => setActiveNode(null)}
              >
                {/* Node Anchor dot */}
                <div
                  className={`w-3.5 h-3.5 rounded-sm flex items-center justify-center border transition-all duration-300 ${
                    isCollected
                      ? 'border-primary bg-primary/20 shadow-[0_0_6px_var(--primary)]'
                      : 'border-border bg-card/85 hover:border-primary/60'
                  } ${isPulsing ? 'scale-125' : ''}`}
                >
                  <div
                    className={`w-1.5 h-1.5 rounded-sm transition-all duration-300 ${
                      isCollected ? 'bg-primary' : 'bg-muted-foreground/30 group-hover:bg-primary/50'
                    }`}
                  />
                </div>

                {/* Node Label */}
                <div
                  className={`absolute left-5 top-1/2 -translate-y-1/2 px-1.5 py-0.5 rounded font-black tracking-wide border transition-all duration-300 select-none whitespace-nowrap ${
                    isCollected
                      ? 'text-primary border-primary/20 bg-primary/5'
                      : 'text-muted-foreground/80 border-transparent hover:text-foreground'
                  }`}
                >
                  {node.label}
                </div>

                {/* Micro tooltip details */}
                {isHovered && (
                  <div className="absolute bottom-6 left-1/2 -translate-x-1/2 bg-popover text-popover-foreground border border-border px-2 py-1 rounded shadow-md z-30 font-mono text-[8px] whitespace-nowrap pointer-events-none">
                    <p className="font-bold text-primary">{node.label} MODULE</p>
                    <p className="text-muted-foreground mt-0.5">{node.desc}</p>
                    <p className="text-[7px] text-emerald-400 mt-0.5">
                      STATUS: {isCollected ? 'COLLECTED & ROUTING' : 'READY / PENDING'}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Sync Complete High-Tech Overlay */}
      <AnimatePresence>
        {showSyncMessage && (
          <motion.div
            initial={{ opacity: 0, backdropFilter: 'blur(0px)' }}
            animate={{ opacity: 1, backdropFilter: 'blur(3px)' }}
            exit={{ opacity: 0, backdropFilter: 'blur(0px)' }}
            className="absolute inset-0 bg-background/80 flex flex-col justify-center items-center font-mono z-20"
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="text-center p-6 border border-primary/30 rounded-xl bg-card max-w-sm shadow-[0_0_24px_rgba(var(--primary-rgb),0.15)]"
            >
              <div className="inline-block relative">
                <span className="absolute -inset-1 rounded bg-primary/20 blur animate-pulse" />
                <h3 className="relative font-pixel text-xs text-primary tracking-widest uppercase">
                  BUILD COMPLETE
                </h3>
              </div>
              <p className="text-[8px] text-muted-foreground mt-3 tracking-widest uppercase leading-relaxed">
                SYSTEM KNOWLEDGE SYNCHRONIZED
              </p>
              <div className="mt-4 flex gap-1 justify-center">
                {Array.from({ length: 16 }).map((_, i) => (
                  <div 
                    key={i} 
                    className="h-1 w-1 bg-primary rounded-sm animate-pulse"
                    style={{ animationDelay: `${i * 80}ms` }}
                  />
                ))}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
