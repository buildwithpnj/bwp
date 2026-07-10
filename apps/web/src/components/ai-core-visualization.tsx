'use client';

import React, { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// ─── Interfaces ───────────────────────────────────────────────────────────────

interface CoreNode {
  id: string;
  label: string;
  x: number;
  y: number;
  desc: string;
  status: string;
}

// ─── Node Configuration ───────────────────────────────────────────────────────

const CORE_NODES: CoreNode[] = [
  { id: 'voice', label: 'Voice AI', x: 108, y: 108, desc: 'Realtime speech synthesis & transcript audio engines', status: 'VOICE READY' },
  { id: 'agents', label: 'AI Agents', x: 70, y: 200, desc: 'Autonomous reasoning, loop planning & execution loops', status: 'AGENTS LOADED' },
  { id: 'mcp', label: 'MCP Link', x: 108, y: 292, desc: 'Model Context Protocol tool protocol bindings', status: 'MCP BOUND' },
  { id: 'vector', label: 'Vector DB', x: 200, y: 330, desc: 'pgvector semantic store index & similarity queries', status: 'DB INDEXED' },
  { id: 'rag', label: 'RAG Pipeline', x: 292, y: 292, desc: 'Document chunking & contextual augment validation', status: 'RAG ACTIVE' },
  { id: 'tools', label: 'Tools Engine', x: 330, y: 200, desc: 'Dynamic sandboxed tool runner & executor runtime', status: 'EXEC READY' },
  { id: 'memory', label: 'Memory', x: 292, y: 108, desc: 'Episodic chat history storage & state summarizer', status: 'MEMORY SYNCD' },
  { id: 'automation', label: 'Automation', x: 200, y: 70, desc: 'Webhook triggers & cross-platform system actions', status: 'CRON NOMINAL' },
];

// Predefined circuit lines with professional 90/45 degree routing bends
const CIRCUITS = [
  { id: 'voice-to-core', path: 'M 108,108 L 154,108 L 175,129 L 175,145', from: 'voice', to: 'core' },
  { id: 'core-to-memory', path: 'M 255,200 L 270,200 L 292,178 L 292,108', from: 'core', to: 'memory' },
  { id: 'memory-to-tools', path: 'M 292,108 L 330,146 L 330,200', from: 'memory', to: 'tools' },
  { id: 'tools-to-rag', path: 'M 330,200 L 330,254 L 292,292', from: 'tools', to: 'rag' },
  { id: 'rag-to-vector', path: 'M 292,292 L 246,292 L 200,330', from: 'rag', to: 'vector' },
  { id: 'vector-to-mcp', path: 'M 200,330 L 154,292 L 108,292', from: 'vector', to: 'mcp' },
  { id: 'mcp-to-agents', path: 'M 108,292 L 70,254 L 70,200', from: 'mcp', to: 'agents' },
  { id: 'agents-to-core', path: 'M 70,200 L 145,200', from: 'agents', to: 'core' },
  { id: 'core-to-automation', path: 'M 200,145 L 200,70', from: 'core', to: 'automation' },
  { id: 'automation-to-voice', path: 'M 200,70 L 154,70 L 108,108', from: 'automation', to: 'voice' },
];

export function AICoreVisualization() {
  const containerRef = useRef<HTMLDivElement>(null);
  const pathRefs = useRef<Record<string, SVGPathElement | null>>({});
  
  const [inViewport, setInViewport] = useState(false);
  const [hoveredNode, setHoveredNode] = useState<CoreNode | null>(null);
  const [statusMsg, setStatusMsg] = useState('SYSTEM ONLINE');
  const [coreActivity, setCoreActivity] = useState(0.3); // 0 to 1 brightness variable

  // Packets state managed directly with refs for perfect performance
  const packetRef = useRef<Record<string, { progress: number; speed: number; delay: number }>>({});
  const animationRef = useRef<number | null>(null);

  // Setup packets structure
  useEffect(() => {
    CIRCUITS.forEach(c => {
      packetRef.current[c.id] = {
        progress: 0,
        speed: 1.0 + Math.random() * 0.8,
        delay: Math.random() * 60,
      };
    });
  }, []);

  // Intersection observer to track viewport state
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        setInViewport(entry.isIntersecting);
      },
      { threshold: 0.1 }
    );
    if (containerRef.current) observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, []);

  // Animation Loop
  useEffect(() => {
    if (!inViewport) {
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
      return;
    }

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;

    // Trigger occasional full network pulse
    let pulseTimer = 0;

    const animate = () => {
      pulseTimer++;
      
      // Update core activity pulse
      setCoreActivity(0.3 + Math.sin(Date.now() * 0.003) * 0.15 + (hoveredNode ? 0.35 : 0));

      if (pulseTimer > 280) {
        // Trigger quick blink status updates
        const randNode = CORE_NODES[Math.floor(Math.random() * CORE_NODES.length)];
        setStatusMsg(randNode.status);
        pulseTimer = 0;
      }

      CIRCUITS.forEach(circuit => {
        const pState = packetRef.current[circuit.id];
        const path = pathRefs.current[circuit.id];
        const dot = document.getElementById(`packet-${circuit.id}`);
        
        if (!pState || !path || !dot) return;

        // If hovered node matches one of connection points, slow or stop packet
        const isInterrupted = hoveredNode && (circuit.from === hoveredNode.id || circuit.to === hoveredNode.id);

        if (pState.delay > 0) {
          pState.delay--;
          dot.style.opacity = '0';
          return;
        }

        dot.style.opacity = '1';
        pState.progress = (pState.progress + (isInterrupted ? 0.25 : pState.speed)) % path.getTotalLength();
        
        const point = path.getPointAtLength(pState.progress);
        dot.style.transform = `translate3d(${point.x}px, ${point.y}px, 0)`;
      });

      animationRef.current = requestAnimationFrame(animate);
    };

    animationRef.current = requestAnimationFrame(animate);
    return () => {
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
    };
  }, [inViewport, hoveredNode]);

  return (
    <div
      ref={containerRef}
      className="w-[320px] h-[320px] sm:w-[400px] sm:h-[400px] relative select-none flex items-center justify-center"
    >
      {/* Blueprint style grid overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(148,163,184,0.03)_1px,transparent_1px),linear-gradient(to_bottom,rgba(148,163,184,0.03)_1px,transparent_1px)] bg-[size:16px_16px] pointer-events-none rounded-xl" />

      {/* SVG Diagram Canvas */}
      <svg
        className="absolute inset-0 w-full h-full pointer-events-none"
        viewBox="0 0 400 400"
      >
        {/* Sub-grid/Circuit details */}
        <circle cx="200" cy="200" r="130" fill="none" stroke="currentColor" className="text-border/20" strokeWidth="1" strokeDasharray="3 6" />
        <circle cx="200" cy="200" r="175" fill="none" stroke="currentColor" className="text-border/10" strokeWidth="0.5" />

        {/* Diagonal axis guides */}
        <line x1="70" y1="70" x2="330" y2="330" stroke="currentColor" className="text-border/10" strokeWidth="0.5" />
        <line x1="330" y1="70" x2="70" y2="330" stroke="currentColor" className="text-border/10" strokeWidth="0.5" />

        {/* Base circuit traces */}
        {CIRCUITS.map((c) => {
          const isHighlighted = hoveredNode && (c.from === hoveredNode.id || c.to === hoveredNode.id);
          return (
            <g key={c.id}>
              {/* Underlying bright track glow */}
              <path
                d={c.path}
                fill="none"
                stroke="var(--primary)"
                className="transition-all duration-300"
                strokeWidth={isHighlighted ? '2.5' : '1'}
                style={{ opacity: isHighlighted ? 0.35 : 0.08 }}
              />
              {/* Outer trace line */}
              <path
                ref={(el) => {
                  pathRefs.current[c.id] = el;
                }}
                d={c.path}
                fill="none"
                stroke="currentColor"
                className={`transition-colors duration-300 ${
                  isHighlighted ? 'text-primary' : 'text-border/40 dark:text-border/20'
                }`}
                strokeWidth="1.2"
              />
            </g>
          );
        })}
      </svg>

      {/* Travelling Packets (glowing micro circles) */}
      {CIRCUITS.map((c) => (
        <div
          key={`dot-${c.id}`}
          id={`packet-${c.id}`}
          className="absolute top-0 left-0 w-[5px] h-[5px] bg-primary rounded-sm shadow-[0_0_6px_var(--primary)] pointer-events-none z-10"
          style={{ margin: '-2.5px 0 0 -2.5px' }}
        />
      ))}

      {/* ─── Animated Central Core Processor ───────────────────────────────── */}
      <div
        className="absolute w-[110px] h-[110px] rounded-xl border border-primary/40 bg-card/85 backdrop-blur-md shadow-[0_0_20px_var(--primary)] flex flex-col items-center justify-center z-20 group transition-all duration-500 hover:scale-105 overflow-hidden"
        style={{
          boxShadow: `0 0 ${24 * coreActivity}px rgba(59, 130, 246, ${coreActivity})`,
        }}
      >
        {/* Internal rotators (positioned behind text via z-[5] and z-[6]) */}
        <div className="absolute inset-2 border border-border/30 rounded-lg animate-[spin_10s_linear_infinite] z-[5]" />
        <div className="absolute inset-4 border border-dashed border-primary/25 rounded-md animate-[spin_6s_linear_infinite_reverse] z-[6]" />
        
        {/* Semi-transparent overlay to separate text from background rotator lines */}
        <div className="absolute inset-0 bg-card/65 backdrop-blur-sm z-[8]" />

        {/* Core Labels (brought to front using z-10) */}
        <div className="font-mono text-[9px] text-muted-foreground/90 tracking-wider z-10 select-none">AI CORE</div>
        <div className="font-pixel text-[11px] text-primary mt-1 tracking-wider animate-pulse z-10 select-none">WARBORN</div>
        <div className="font-mono text-[8px] text-emerald-400 mt-1 font-bold z-10 select-none">1.4 TFLOP</div>

        {/* Digital scan line (brought to front using z-10) */}
        <div 
          className="absolute left-0 right-0 h-[1.5px] bg-gradient-to-r from-transparent via-cyan-400 to-transparent shadow-[0_0_6px_rgba(34,211,238,0.8)] z-10"
          style={{
            animation: 'scanLine 4s cubic-bezier(0.4, 0, 0.2, 1) infinite',
            top: '0%'
          }}
        />
      </div>

      {/* ─── Surrounding Nodes ────────────────────────────────────────────── */}
      {CORE_NODES.map((node) => {
        const isHovered = hoveredNode?.id === node.id;
        return (
          <div
            key={node.id}
            className="absolute font-mono text-[8px] transition-all duration-300"
            style={{
              left: `${(node.x / 400) * 100}%`,
              top: `${(node.y / 400) * 100}%`,
              transform: 'translate(-50%, -50%)',
              zIndex: isHovered ? 40 : 10
            }}
            onMouseEnter={() => setHoveredNode(node)}
            onMouseLeave={() => setHoveredNode(null)}
          >
            <div className="flex flex-col items-center gap-1">
              {/* Circle Anchor */}
              <div
                className={`w-[18px] h-[18px] rounded-md border flex items-center justify-center transition-all duration-300 shadow-sm ${
                  isHovered 
                    ? 'border-primary bg-primary/20 scale-110 shadow-[0_0_8px_var(--primary)]' 
                    : 'border-border bg-card/90 hover:border-primary/50'
                }`}
              >
                <div className={`w-1.5 h-1.5 rounded-sm transition-all duration-300 ${isHovered ? 'bg-primary' : 'bg-muted-foreground/45'}`} />
              </div>

              {/* Text label */}
              <div 
                className={`px-1.5 py-0.5 rounded font-black tracking-wide border transition-all duration-300 select-none whitespace-nowrap bg-card/60 backdrop-blur-sm ${
                  isHovered ? 'text-primary border-primary/20' : 'text-muted-foreground/95 border-transparent'
                }`}
              >
                {node.label}
              </div>
            </div>

            {/* Hover Tooltip Overlay */}
            {isHovered && (
              <div className="absolute bottom-10 left-1/2 -translate-x-1/2 bg-popover text-popover-foreground border border-border px-2 py-1.5 rounded-lg shadow-md z-30 font-mono text-[8px] w-[140px] whitespace-normal pointer-events-none">
                <p className="font-bold text-primary uppercase text-[7px]">{node.label}</p>
                <p className="text-muted-foreground mt-0.5 leading-normal">{node.desc}</p>
                <p className="text-emerald-400 mt-1 scale-90 font-semibold tracking-wider">{node.status}</p>
              </div>
            )}
          </div>
        );
      })}

      {/* Engineering Info Box Overlay */}
      <div className="absolute bottom-2 left-2 right-2 flex justify-between items-center font-mono text-[7px] text-muted-foreground/60 border border-border/20 bg-card/10 px-2 py-1 rounded">
        <span>CORE TEMP: 34°C</span>
        <span className="text-primary font-bold">{statusMsg}</span>
      </div>
    </div>
  );
}
