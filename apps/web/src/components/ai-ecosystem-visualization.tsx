'use client';

import React, { useState, useEffect, useRef } from 'react';
import { 
  Brain, 
  Cpu, 
  Layers, 
  Network, 
  Activity, 
  Terminal, 
  Zap, 
  ChevronRight,
  Sparkles,
  Server,
  Database
} from 'lucide-react';
import { cn } from '@/lib/utils';

// Types
interface ProductCard {
  name: string;
  status: 'LIVE' | 'BUILDING' | 'DEPLOYED' | 'ACTIVE' | 'ONLINE';
  desc: string;
  version?: string;
}

export function AiEcosystemCommandCenter() {
  const [activeTab, setActiveTab] = useState<'core' | 'products' | 'tech'>('core');
  
  // Real-time ticking metrics state
  const [metrics, setMetrics] = useState({
    agentsRunning: 14,
    memorySize: 4.82,
    activeWorkflows: 38,
    apiRequests: 14205,
    modelCalls: 28912,
    automationJobs: 843,
    responseTime: 128,
    latency: 24
  });

  // Randomize metrics to simulate active ecosystem
  useEffect(() => {
    const timer = setInterval(() => {
      setMetrics((prev) => {
        const reqIncrement = Math.floor(Math.random() * 3) + 1;
        const callIncrement = Math.floor(Math.random() * 5) + 2;
        const jobIncrement = Math.random() < 0.3 ? 1 : 0;
        
        return {
          agentsRunning: Math.min(24, Math.max(10, prev.agentsRunning + (Math.random() < 0.2 ? (Math.random() < 0.5 ? 1 : -1) : 0))),
          memorySize: parseFloat((prev.memorySize + (Math.random() < 0.05 ? 0.01 : 0)).toFixed(2)),
          activeWorkflows: Math.min(50, Math.max(30, prev.activeWorkflows + (Math.random() < 0.1 ? (Math.random() < 0.5 ? 1 : -1) : 0))),
          apiRequests: prev.apiRequests + reqIncrement,
          modelCalls: prev.modelCalls + callIncrement,
          automationJobs: prev.automationJobs + jobIncrement,
          responseTime: Math.floor(120 + Math.sin(Date.now() / 5000) * 12 + Math.random() * 4),
          latency: Math.floor(22 + Math.cos(Date.now() / 3000) * 3 + Math.random() * 2)
        };
      });
    }, 2500);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="w-full h-full flex flex-col gap-5 border border-border/30 bg-card/40 backdrop-blur-md rounded-2xl p-5 md:p-6 shadow-2xl relative overflow-hidden group select-none">
      {/* Tech Grid Background Lines overlay */}
      <div className="absolute inset-0 bg-grid-dots opacity-[0.25] pointer-events-none" />
      
      {/* Decorative Corner HUD Brackets */}
      <div className="absolute top-3 left-3 w-4 h-4 border-t-2 border-l-2 border-primary/40 rounded-tl" />
      <div className="absolute top-3 right-3 w-4 h-4 border-t-2 border-r-2 border-primary/40 rounded-tr" />
      <div className="absolute bottom-3 left-3 w-4 h-4 border-b-2 border-l-2 border-primary/40 rounded-bl" />
      <div className="absolute bottom-3 right-3 w-4 h-4 border-b-2 border-r-2 border-primary/40 rounded-br" />

      {/* Cybernetic HUD Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-border/20 pb-4 z-10">
        <div className="flex items-center gap-2.5">
          <Terminal className="h-4.5 w-4.5 text-primary animate-pulse" />
          <div className="flex flex-col">
            <span className="font-pixel text-[10px] tracking-[0.2em] text-primary uppercase">{"// COGNITIVE COMMAND"}</span>
            <span className="font-mono text-xs text-foreground/80 font-bold uppercase tracking-wider">SYSTEM HUD V3.5.0</span>
          </div>
        </div>
        
        {/* Terminal Tab Switchers */}
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-background/50 border border-border/40 font-mono text-2xs">
          <button
            onClick={() => setActiveTab('core')}
            className={cn(
              "px-3 py-1.5 rounded-lg font-bold transition-all uppercase tracking-wider",
              activeTab === 'core' 
                ? "bg-primary text-primary-foreground shadow-sm shadow-primary/20" 
                : "text-muted-foreground hover:text-foreground hover:bg-secondary/40"
            )}
          >
            [ CORE ]
          </button>
          <button
            onClick={() => setActiveTab('products')}
            className={cn(
              "px-3 py-1.5 rounded-lg font-bold transition-all uppercase tracking-wider",
              activeTab === 'products' 
                ? "bg-primary text-primary-foreground shadow-sm shadow-primary/20" 
                : "text-muted-foreground hover:text-foreground hover:bg-secondary/40"
            )}
          >
            [ PRODUCTS ]
          </button>
          <button
            onClick={() => setActiveTab('tech')}
            className={cn(
              "px-3 py-1.5 rounded-lg font-bold transition-all uppercase tracking-wider",
              activeTab === 'tech' 
                ? "bg-primary text-primary-foreground shadow-sm shadow-primary/20" 
                : "text-muted-foreground hover:text-foreground hover:bg-secondary/40"
            )}
          >
            [ TECH ]
          </button>
        </div>
      </div>

      {/* Main Tab Render Body */}
      <div className="flex-1 w-full overflow-hidden z-10 relative">
        {activeTab === 'core' && <TabNeuralCore metrics={metrics} />}
        {activeTab === 'products' && <TabProductsFlow />}
        {activeTab === 'tech' && <TabTechEcosystem />}
      </div>
    </div>
  );
}

/* ============================================================================
   SUB-COMPONENT: Tab 1 - Neural Core, LLMs, and System Metrics
   ============================================================================ */
function TabNeuralCore({ metrics }: { metrics: any }) {
  const capabilities = [
    'Reasoning', 'Planning', 'Memory', 'Tool Calling', 
    'Orchestration', 'Evaluation', 'Context Eng', 'Prompt Eng',
    'Agent Collab', 'Workflow Eng', 'Vector Search', 'Retrieval'
  ];

  const llmProviders = [
    { name: 'Claude', glow: 'rgba(124, 58, 237, 0.25)' },
    { name: 'Gemini', glow: 'rgba(59, 130, 246, 0.25)' },
    { name: 'OpenAI', glow: 'rgba(6, 182, 212, 0.25)' },
    { name: 'Llama', glow: 'rgba(16, 185, 129, 0.25)' },
    { name: 'Mistral', glow: 'rgba(245, 158, 11, 0.25)' },
    { name: 'DeepSeek', glow: 'rgba(59, 130, 246, 0.25)' },
    { name: 'Ollama', glow: 'rgba(124, 58, 237, 0.25)' },
    { name: 'Hugging Face', glow: 'rgba(245, 158, 11, 0.25)' }
  ];

  return (
    <div className="w-full h-full flex flex-col gap-5 justify-between">
      <div className="grid grid-cols-1 md:grid-cols-12 gap-5 items-center flex-1">
        {/* SVG Centered Neural AI Core Map */}
        <div className="md:col-span-7 flex justify-center items-center h-full min-h-[220px]">
          <svg className="w-full max-w-[280px] aspect-square overflow-visible" viewBox="0 0 300 300">
            {/* Pulsing Concentric Background Rings */}
            <circle cx="150" cy="150" r="100" fill="none" stroke="rgba(59, 130, 246, 0.04)" strokeWidth="1.5" />
            <circle cx="150" cy="150" r="70" fill="none" stroke="rgba(6, 182, 212, 0.06)" strokeWidth="1.5" />
            
            <defs>
              <radialGradient id="core-glow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#06B6D4" stopOpacity="0.4" />
                <stop offset="70%" stopColor="#2563EB" stopOpacity="0.1" />
                <stop offset="100%" stopColor="#000000" stopOpacity="0" />
              </radialGradient>
            </defs>
            <circle cx="150" cy="150" r="50" fill="url(#core-glow)" className="animate-pulse" />
            
            {/* Outgoing Connective Links with animation */}
            {capabilities.map((_, i) => {
              const angle = (i * 2 * Math.PI) / capabilities.length;
              const x = 150 + Math.cos(angle) * 110;
              const y = 150 + Math.sin(angle) * 110;
              return (
                <g key={i} className="group/link">
                  <line 
                    x1="150" 
                    y1="150" 
                    x2={x} 
                    y2={y} 
                    stroke="rgba(6, 182, 212, 0.15)" 
                    strokeWidth="1" 
                    className="group-hover/link:stroke-primary/50 transition-colors"
                  />
                  <line 
                    x1="150" 
                    y1="150" 
                    x2={x} 
                    y2={y} 
                    stroke="#06B6D4" 
                    strokeWidth="1.5" 
                    strokeDasharray="6 35"
                    className="opacity-60"
                  >
                    <animate 
                      attributeName="stroke-dashoffset" 
                      values="0;41" 
                      dur="3s" 
                      repeatCount="indefinite" 
                    />
                  </line>
                </g>
              );
            })}

            {/* Central Glowing AI Core node */}
            <g className="cursor-pointer">
              <circle cx="150" cy="150" r="28" fill="#0B1020" stroke="url(#cyan-blue-grad)" strokeWidth="2" className="shadow-lg shadow-cyan-500/20" />
              <circle cx="150" cy="150" r="18" fill="rgba(6, 182, 212, 0.1)" stroke="#06B6D4" strokeWidth="1.5" className="animate-ping" style={{ animationDuration: '4s' }} />
              <text x="150" y="146" fill="#FFFFFF" textAnchor="middle" className="font-pixel text-[8px] font-bold tracking-widest">AI</text>
              <text x="150" y="157" fill="#06B6D4" textAnchor="middle" className="font-pixel text-[7px] font-semibold tracking-wider">CORE</text>
            </g>

            {/* Gradients */}
            <defs>
              <linearGradient id="cyan-blue-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#06B6D4" />
                <stop offset="100%" stopColor="#2563EB" />
              </linearGradient>
            </defs>

            {/* Outlying Capability Labels */}
            {capabilities.map((label, i) => {
              const angle = (i * 2 * Math.PI) / capabilities.length;
              const x = 150 + Math.cos(angle) * 114;
              const y = 150 + Math.sin(angle) * 114;
              const isRight = Math.cos(angle) >= 0;
              return (
                <g key={i}>
                  {/* Subtle node dot */}
                  <circle cx={x} cy={y} r="2.5" fill={i % 3 === 0 ? '#8B5CF6' : '#06B6D4'} />
                  {/* Glowing text node */}
                  <text 
                    x={x + (isRight ? 6 : -6)} 
                    y={y + 3} 
                    fill="rgba(255,255,255,0.75)" 
                    textAnchor={isRight ? 'start' : 'end'} 
                    className="font-mono text-[8px] font-bold tracking-wide uppercase hover:fill-primary transition-colors cursor-default"
                  >
                    {label}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>

        {/* Live HUD Metrics Panel */}
        <div className="md:col-span-5 grid grid-cols-2 gap-3 h-fit border-l border-border/15 pl-0 md:pl-5">
          <MetricHUDItem label="Agents Running" value={metrics.agentsRunning} suffix=" ACTIVE" color="text-primary" />
          <MetricHUDItem label="Memory Pool" value={metrics.memorySize} suffix=" TB" color="text-purple-400" />
          <MetricHUDItem label="Active Workflows" value={metrics.activeWorkflows} suffix=" PIPES" color="text-cyan-400" />
          <MetricHUDItem label="Automation Jobs" value={metrics.automationJobs} suffix=" LOGGED" color="text-emerald-400" />
          <MetricHUDItem label="API Ingress" value={metrics.apiRequests.toLocaleString()} suffix="" color="text-foreground" isLong />
          <MetricHUDItem label="Model Inferences" value={metrics.modelCalls.toLocaleString()} suffix="" color="text-foreground" isLong />
          <MetricHUDItem label="Avg Response" value={metrics.responseTime} suffix="ms" color="text-emerald-400" />
          <MetricHUDItem label="Internal Latency" value={metrics.latency} suffix="ms" color="text-cyan-400" />
        </div>
      </div>

      {/* LLM Providers Strip */}
      <div className="border-t border-border/20 pt-4 flex flex-col gap-2">
        <span className="font-pixel text-[8px] tracking-[0.25em] text-muted-foreground/80">{"// LLM COMPILER REGISTRY"}</span>
        <div className="flex flex-wrap items-center gap-1.5 sm:gap-2.5">
          {llmProviders.map((llm) => (
            <div 
              key={llm.name}
              className="px-2.5 py-1.5 rounded-lg border border-border/40 bg-background/40 font-mono text-[9px] font-bold text-foreground/80 hover:text-foreground hover:border-primary/30 transition-all hover:scale-[1.03] cursor-default flex items-center gap-1.5"
              style={{ boxShadow: `inset 0 0 4px ${llm.glow}` }}
            >
              <div className="w-1 h-1 rounded-full bg-primary" />
              <span>{llm.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function MetricHUDItem({ label, value, suffix, color, isLong }: { label: string; value: string | number; suffix: string; color: string; isLong?: boolean }) {
  return (
    <div className={cn("flex flex-col p-2.5 rounded-xl border border-border/30 bg-background/30 font-mono text-left", isLong && "col-span-2")}>
      <span className="text-[8px] text-muted-foreground tracking-wider uppercase">{label}</span>
      <div className="flex items-baseline gap-1 mt-0.5">
        <span className={cn("text-sm sm:text-base font-extrabold tracking-tight", color)}>{value}</span>
        {suffix && <span className="text-[8px] text-muted-foreground font-bold">{suffix}</span>}
      </div>
    </div>
  );
}

/* ============================================================================
   SUB-COMPONENT: Tab 2 - AI Products List & Pipeline Flow
   ============================================================================ */
function TabProductsFlow() {
  const products: ProductCard[] = [
    { name: 'AI Voice Agent', status: 'LIVE', desc: 'Real-time dual-latency conversational voice engine.', version: 'v1.4' },
    { name: 'Warborn OS', status: 'BUILDING', desc: 'Agentic desktop execution environment.', version: 'v0.2' },
    { name: 'AI Growth Agent', status: 'DEPLOYED', desc: 'Autonomous lead scraping, enrichment & outreach.', version: 'v2.1' },
    { name: 'AI Automation Platform', status: 'ACTIVE', desc: 'Webhooks & trigger routing execution pipes.', version: 'v1.0' },
    { name: 'Customer Support AI', status: 'ONLINE', desc: 'Multi-agent CRM ticket resolver & routing.', version: 'v1.8' },
    { name: 'RAG Intelligence', status: 'ACTIVE', desc: 'Vector-indexed hybrid semantic search search.', version: 'v2.0' },
    { name: 'Memory Engine', status: 'ACTIVE', desc: 'Persistent cross-session entity extraction & DB.', version: 'v1.2' },
    { name: 'Voice Receptionist', status: 'LIVE', desc: '24/7 inbound call routing & calendar sync.', version: 'v1.5' }
  ];

  return (
    <div className="w-full h-full flex flex-col gap-4 overflow-y-auto pr-1">
      {/* Products Grid */}
      <div className="grid grid-cols-2 gap-3 flex-1">
        {products.map((p, idx) => (
          <ProductGlassCard key={idx} product={p} />
        ))}
      </div>

      {/* Architecture Flow SVG block */}
      <div className="flex flex-col gap-2 mt-2 border-t border-border/20 pt-4">
        <span className="font-pixel text-[8px] tracking-[0.25em] text-muted-foreground/80">{"// PIPELINE ORCHESTRATION ARCHITECTURE"}</span>
        <div className="relative w-full border border-border/30 bg-background/30 rounded-xl p-3 h-[70px] overflow-hidden flex items-center">
          
          {/* SVG Animated Connection Flow Line */}
          <svg className="absolute inset-0 w-full h-full pointer-events-none" preserveAspectRatio="none" viewBox="0 0 600 70">
            <path 
              id="arch-flow-path"
              d="M 20,35 H 580" 
              fill="none" 
              stroke="rgba(6, 182, 212, 0.12)" 
              strokeWidth="2" 
            />
            {/* Secondary pulsing path */}
            <path 
              d="M 20,35 H 580" 
              fill="none" 
              stroke="url(#flow-line-grad)" 
              strokeWidth="1.5" 
              strokeDasharray="15 150"
              className="opacity-70"
            >
              <animate 
                attributeName="stroke-dashoffset" 
                values="0;-165" 
                dur="4s" 
                repeatCount="indefinite" 
              />
            </path>
            
            {/* Flow line gradient definitions */}
            <defs>
              <linearGradient id="flow-line-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#3B82F6" stopOpacity="0.2" />
                <stop offset="50%" stopColor="#06B6D4" stopOpacity="1" />
                <stop offset="100%" stopColor="#8B5CF6" stopOpacity="0.2" />
              </linearGradient>
            </defs>

            {/* Glowing flowing circular particle */}
            <circle r="3.5" fill="#06B6D4" className="shadow-sm shadow-cyan-400">
              <animateMotion dur="4.2s" repeatCount="indefinite">
                <mpath href="#arch-flow-path" />
              </animateMotion>
            </circle>
            <circle r="2" fill="#FFFFFF">
              <animateMotion dur="4.2s" repeatCount="indefinite">
                <mpath href="#arch-flow-path" />
              </animateMotion>
            </circle>
          </svg>

          {/* Flow Node Labels Row */}
          <div className="w-full flex items-center justify-between z-10 px-2 font-mono text-[7px] sm:text-[8px] font-bold text-foreground/75">
            <span className="px-2 py-1 rounded border border-cyan-500/20 bg-background/80 shadow shadow-cyan-500/5">Voice AI</span>
            <span className="text-muted-foreground/40 font-pixel">&gt;&gt;</span>
            <span className="px-2 py-1 rounded border border-primary/20 bg-background/80">AI Core</span>
            <span className="text-muted-foreground/40 font-pixel">&gt;&gt;</span>
            <span className="px-2 py-1 rounded border border-purple-500/20 bg-background/80">RAG</span>
            <span className="text-muted-foreground/40 font-pixel">&gt;&gt;</span>
            <span className="px-2 py-1 rounded border border-yellow-500/20 bg-background/80">LLMs</span>
            <span className="text-muted-foreground/40 font-pixel">&gt;&gt;</span>
            <span className="px-2 py-1 rounded border border-emerald-500/20 bg-background/80">Database</span>
            <span className="text-muted-foreground/40 font-pixel">&gt;&gt;</span>
            <span className="px-2 py-1 rounded border border-cyan-500/25 bg-background/80 text-cyan-400 font-extrabold uppercase">User</span>
          </div>

        </div>
      </div>
    </div>
  );
}

function ProductGlassCard({ product }: { product: ProductCard }) {
  const [tilt, setTilt] = useState({ x: 0, y: 0 });
  const cardRef = useRef<HTMLDivElement>(null);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = (e.clientX - rect.left - rect.width / 2) / (rect.width / 2);
    const y = (e.clientY - rect.top - rect.height / 2) / (rect.height / 2);
    
    // Scale down rotation angles to keep it subtle (max 4.5 degrees)
    setTilt({ x: x * 4.5, y: -y * 4.5 });
  };

  const handleMouseLeave = () => {
    setTilt({ x: 0, y: 0 });
  };

  const statusColor = 
    product.status === 'LIVE' || product.status === 'ONLINE' ? 'bg-emerald-500' :
    product.status === 'BUILDING' ? 'bg-amber-500 animate-pulse' :
    'bg-primary';

  const transformStyle = {
    transform: `perspective(400px) rotateX(${tilt.y}deg) rotateY(${tilt.x}deg) translateZ(2px)`,
    transition: tilt.x === 0 && tilt.y === 0 ? 'transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)' : 'none'
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={transformStyle}
      className="p-3.5 rounded-xl border border-border/30 bg-card/60 hover:bg-card/95 hover:border-primary/20 backdrop-blur-md text-left flex flex-col justify-between gap-1.5 transition-all shadow-md hover:shadow-lg hover:shadow-primary/5 cursor-default relative overflow-hidden group/card"
    >
      {/* Edge lighting glow hover overlay */}
      <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-primary/5 to-cyan-500/5 opacity-0 group-hover/card:opacity-100 transition-opacity pointer-events-none" />

      <div className="flex items-center justify-between gap-1.5 w-full">
        <div className="flex items-center gap-1.5">
          <span className={cn("w-1.5 h-1.5 rounded-full", statusColor)} />
          <span className="font-pixel text-[8px] font-bold text-foreground/80 tracking-wide">{product.status}</span>
        </div>
        {product.version && (
          <span className="font-mono text-[7px] text-muted-foreground font-bold px-1.5 py-0.5 rounded bg-background/50 border border-border/40">
            {product.version}
          </span>
        )}
      </div>

      <h4 className="font-mono text-[10px] sm:text-xs font-black text-foreground uppercase tracking-tight group-hover/card:text-primary transition-colors">
        {product.name}
      </h4>

      <p className="text-[9px] sm:text-[10px] leading-relaxed text-muted-foreground/90 font-medium">
        {product.desc}
      </p>
    </div>
  );
}

/* ============================================================================
   SUB-COMPONENT: Tab 3 - Tech Stack Neural Network
   ============================================================================ */
interface TechNode {
  name: string;
  category: 'frontend' | 'backend' | 'database' | 'ai' | 'tools';
  x: number;
  y: number;
}

function TabTechEcosystem() {
  const [hoverCategory, setHoverCategory] = useState<string | null>(null);

  // Nodes coordinated statically to form a beautiful network mesh
  const nodes: TechNode[] = [
    // Center Hub Categories
    { name: 'FRONTEND', category: 'frontend', x: 75, y: 70 },
    { name: 'BACKEND', category: 'backend', x: 225, y: 70 },
    { name: 'AI / LLM', category: 'ai', x: 150, y: 140 },
    { name: 'DATABASES', category: 'database', x: 75, y: 210 },
    { name: 'DEV TOOLS', category: 'tools', x: 225, y: 210 },

    // Frontend Nodes
    { name: 'Next.js', category: 'frontend', x: 30, y: 40 },
    { name: 'React', category: 'frontend', x: 45, y: 100 },
    { name: 'Tailwind CSS', category: 'frontend', x: 120, y: 40 },

    // Backend Nodes
    { name: 'FastAPI', category: 'backend', x: 270, y: 40 },
    { name: 'Python', category: 'backend', x: 180, y: 40 },
    { name: 'WebSockets', category: 'backend', x: 255, y: 100 },

    // AI Nodes
    { name: 'LangGraph', category: 'ai', x: 100, y: 140 },
    { name: 'Claude', category: 'ai', x: 150, y: 90 },
    { name: 'Gemini', category: 'ai', x: 200, y: 140 },
    { name: 'Ollama', category: 'ai', x: 150, y: 185 },

    // Databases Nodes
    { name: 'PostgreSQL', category: 'database', x: 30, y: 180 },
    { name: 'Redis', category: 'database', x: 120, y: 240 },
    { name: 'pgvector', category: 'database', x: 30, y: 240 },

    // Tools Nodes
    { name: 'Docker', category: 'tools', x: 270, y: 180 },
    { name: 'Git', category: 'tools', x: 180, y: 240 },
    { name: 'MCP', category: 'tools', x: 270, y: 240 }
  ];

  // Interconnection links
  const links = [
    { from: 0, to: 1 }, { from: 0, to: 2 }, { from: 1, to: 2 },
    { from: 3, to: 2 }, { from: 4, to: 2 }, { from: 3, to: 4 },

    // Frontend links
    { from: 0, to: 5 }, { from: 0, to: 6 }, { from: 0, to: 7 },
    // Backend links
    { from: 1, to: 8 }, { from: 1, to: 9 }, { from: 1, to: 10 },
    // AI links
    { from: 2, to: 11 }, { from: 2, to: 12 }, { from: 2, to: 13 }, { from: 2, to: 14 },
    // Database links
    { from: 3, to: 15 }, { from: 3, to: 16 }, { from: 3, to: 17 },
    // Tools links
    { from: 4, to: 18 }, { from: 4, to: 19 }, { from: 4, to: 20 }
  ];

  const getCategoryColor = (cat: string, isText = false) => {
    if (hoverCategory && hoverCategory !== cat) {
      return isText ? 'fill-muted-foreground/30 text-muted-foreground/30' : 'rgba(255,255,255,0.05)';
    }
    switch (cat) {
      case 'frontend': return isText ? 'fill-blue-400 text-blue-400' : '#3B82F6';
      case 'backend': return isText ? 'fill-purple-400 text-purple-400' : '#8B5CF6';
      case 'ai': return isText ? 'fill-cyan-400 text-cyan-400' : '#06B6D4';
      case 'database': return isText ? 'fill-emerald-400 text-emerald-400' : '#10B981';
      case 'tools': return isText ? 'fill-yellow-400 text-yellow-400' : '#F59E0B';
      default: return isText ? 'fill-foreground text-foreground' : 'white';
    }
  };

  return (
    <div className="w-full h-full flex flex-col justify-between select-none">
      {/* Category Highlighter Filter Menu */}
      <div className="flex items-center gap-1.5 flex-wrap font-mono text-[8px] font-bold border-b border-border/10 pb-3">
        <span className="text-muted-foreground/80 tracking-wider">HIGHLIGHT LAYER:</span>
        {['FRONTEND', 'BACKEND', 'AI', 'DATABASE', 'TOOLS'].map((cat) => {
          const catKey = cat.toLowerCase() === 'database' ? 'database' : cat.toLowerCase();
          const isActive = hoverCategory === catKey;
          return (
            <button
              key={cat}
              onMouseEnter={() => setHoverCategory(catKey)}
              onMouseLeave={() => setHoverCategory(null)}
              className={cn(
                "px-2 py-1 rounded border border-border/40 transition-colors uppercase",
                isActive ? "bg-primary text-primary-foreground border-primary/50" : "bg-background/40 hover:bg-secondary/40 text-muted-foreground hover:text-foreground"
              )}
            >
              {cat}
            </button>
          );
        })}
      </div>

      {/* SVG Neural Mesh Rendering */}
      <div className="flex-1 flex items-center justify-center min-h-[220px]">
        <svg className="w-full max-w-[320px] aspect-[4/3] overflow-visible" viewBox="0 0 300 280">
          
          {/* Drawing Connective Links */}
          {links.map((link, i) => {
            const fromNode = nodes[link.from];
            const toNode = nodes[link.to];
            
            // Fade out links if not related to highlighted category
            const isHighlighted = !hoverCategory || (fromNode.category === hoverCategory && toNode.category === hoverCategory);
            const opacity = isHighlighted ? 0.35 : 0.05;
            const strokeColor = isHighlighted ? getCategoryColor(fromNode.category) : 'rgba(255, 255, 255, 0.1)';

            return (
              <line 
                key={i}
                x1={fromNode.x}
                y1={fromNode.y}
                x2={toNode.x}
                y2={toNode.y}
                stroke={strokeColor}
                strokeWidth={isHighlighted ? 1.2 : 0.8}
                style={{ opacity, transition: 'all 0.3s ease' }}
              />
            );
          })}

          {/* Drawing Interactive Nodes */}
          {nodes.map((node, i) => {
            const isCenterHub = i < 5;
            const isHighlighted = !hoverCategory || node.category === hoverCategory;
            const size = isCenterHub ? 6 : 3.5;
            const nodeColor = getCategoryColor(node.category);
            
            return (
              <g 
                key={i}
                onMouseEnter={() => setHoverCategory(node.category)}
                onMouseLeave={() => setHoverCategory(null)}
                className="cursor-pointer group/node"
              >
                {/* Node Glow Backdrop */}
                {isHighlighted && (
                  <circle 
                    cx={node.x} 
                    cy={node.y} 
                    r={size * 2.5} 
                    fill={nodeColor} 
                    className="opacity-10 group-hover/node:opacity-30 transition-opacity animate-pulse" 
                  />
                )}
                
                {/* Core Node Circle */}
                <circle 
                  cx={node.x} 
                  cy={node.y} 
                  r={size} 
                  fill={isHighlighted ? nodeColor : 'rgba(255,255,255,0.1)'} 
                  stroke={isHighlighted ? '#FFFFFF' : 'none'}
                  strokeWidth="0.8"
                  style={{ transition: 'all 0.3s ease' }}
                />

                {/* Node Label Text */}
                <text
                  x={node.x}
                  y={node.y + (isCenterHub ? -10 : 12)}
                  textAnchor="middle"
                  className={cn(
                    isCenterHub ? "font-pixel text-[8px] font-black uppercase tracking-wider" : "font-mono text-[7px] font-bold tracking-tight",
                    getCategoryColor(node.category, true)
                  )}
                  style={{ transition: 'all 0.3' }}
                >
                  {node.name}
                </text>
              </g>
            );
          })}

        </svg>
      </div>
    </div>
  );
}
