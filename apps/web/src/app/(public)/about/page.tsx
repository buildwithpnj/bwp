import React from 'react';
import Link from 'next/link';
import { 
  ArrowRight, 
  Terminal, 
  Lightbulb, 
  Compass, 
  Cpu, 
  Database, 
  Server, 
  ShieldCheck, 
  CheckCircle2, 
  Circle,
  Code2
} from 'lucide-react';

export const metadata = {
  title: 'About — BuildWithPNJ',
  description: 'Prakash Nandan Jha (PNJ), AI Engineer building production-ready tools in public. Read about my origin story, values, and targets.',
};

export default function PublicAboutPage() {
  return (
    <div className="flex flex-col gap-16 md:gap-24 text-left max-w-5xl mx-auto py-8">
      
      {/* 1. PROFILE / HEADER SECTION */}
      <section className="flex flex-col lg:flex-row items-center lg:items-start gap-12 border-b border-border/40 pb-16">
        
        {/* Left Side: Photo Frame / Avatar */}
        <div className="relative group shrink-0 select-none">
          <div className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-primary to-purple-600 opacity-20 blur group-hover:opacity-40 transition duration-300" />
          
          <div className="relative w-36 h-36 sm:w-44 sm:h-44 rounded-2xl border border-border/50 bg-card/40 backdrop-blur flex flex-col items-center justify-center p-6 shadow-2xl">
            <div className="w-16 h-16 rounded-xl bg-primary/5 flex items-center justify-center border border-primary/10 mb-3 group-hover:scale-105 transition-transform">
              <Code2 className="h-8 w-8 text-primary" />
            </div>
            <span className="font-pixel text-xl text-foreground tracking-widest">PNJ</span>
            <span className="font-mono text-[8px] text-primary mt-1 tracking-wider uppercase">{"// HOST CORE ACTIVE"}</span>
          </div>
        </div>

        {/* Right Side: Bio */}
        <div className="flex-1 flex flex-col gap-4">
          <div className="font-mono text-[9px] text-primary/80 tracking-[0.25em] uppercase font-bold">
            {"// ENGINEER PROFILE"}
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-foreground">
            Prakash Nandan Jha
          </h1>
          <p className="text-sm font-mono text-muted-foreground -mt-2">
            Principal AI Product Engineer @ BuildWithPNJ
          </p>
          <p className="text-sm sm:text-base text-muted-foreground leading-relaxed mt-2">
            I architect autonomous AI agents, stateful vector search pipelines, and local-first workflow engines. My focus is on deploying secure, database-driven systems that solve daily operational bottlenecks—then publishing the complete architectural designs in public.
          </p>
          
          {/* Quick Hardware/Stack Telemetry HUD */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-4 p-4 rounded-xl border border-border/30 bg-card/25 backdrop-blur-sm font-mono text-[9px]">
            <div className="flex flex-col gap-0.5">
              <span className="text-muted-foreground uppercase text-[8px]">LOCAL CORE</span>
              <span className="text-foreground font-black flex items-center gap-1">
                <Cpu className="h-3 w-3 text-primary" /> Llama-3-8B
              </span>
            </div>
            <div className="flex flex-col gap-0.5">
              <span className="text-muted-foreground uppercase text-[8px]">VECTOR DB</span>
              <span className="text-foreground font-black flex items-center gap-1">
                <Database className="h-3 w-3 text-primary" /> pgvector
              </span>
            </div>
            <div className="flex flex-col gap-0.5">
              <span className="text-muted-foreground uppercase text-[8px]">SERVER FRAME</span>
              <span className="text-foreground font-black flex items-center gap-1">
                <Server className="h-3 w-3 text-primary" /> FastAPI/Celery
              </span>
            </div>
            <div className="flex flex-col gap-0.5">
              <span className="text-muted-foreground uppercase text-[8px]">SECURITY</span>
              <span className="text-foreground font-black flex items-center gap-1">
                <ShieldCheck className="h-3 w-3 text-emerald-400" /> OAuth / JWT
              </span>
            </div>
          </div>
        </div>

      </section>

      {/* 2. STORY & CORE VALUES SECTION */}
      <section className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16">
        
        {/* Story Content */}
        <div className="lg:col-span-7 flex flex-col gap-6">
          <div className="flex items-center gap-2">
            <span className="font-mono text-[10px] tracking-[0.25em] text-primary/80 uppercase">
              {"// CHRONICLES"}
            </span>
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-foreground -mt-3">
            Why I Build in the Open
          </h2>
          
          <div className="text-xs sm:text-sm text-muted-foreground leading-relaxed flex flex-col gap-5">
            <p>
              I got into coding because I wanted to solve my own problems. What started as simple command-line scripts to automate backups and file organization evolved into a fascination with local models and vector indexing.
            </p>
            <p>
              During this journey, I noticed a persistent gap: most tutorials stopped at simple notebook scripts or toy chat interfaces. They hid the messy reality of production systems—rate limits, async task queues, memory context leaks, and vector similarity tuning.
            </p>
            <blockquote className="border-l-2 border-primary pl-4 my-2 italic text-foreground/90 font-medium">
              "BuildWithPNJ is a commitment to building production-ready, self-hostable tools that power operations—and sharing every blueprint along the way."
            </blockquote>
            <p>
              By documenting every schema decision, pipeline failure, and performance patch, I hope to demystify complex AI agent deployments for other product builders.
            </p>
          </div>
        </div>

        {/* Core Values Sidebar */}
        <div className="lg:col-span-5 p-6 rounded-2xl border border-border/40 bg-card/35 backdrop-blur-md flex flex-col gap-6 h-fit shadow-lg shadow-black/5">
          <div className="flex items-center gap-2">
            <span className="font-mono text-[9px] tracking-[0.25em] text-primary/80 uppercase font-bold">
              {"// OPERATIONAL PRINCIPLES"}
            </span>
          </div>
          
          <div className="flex flex-col gap-4 text-xs">
            {/* Value 1 */}
            <div className="flex items-start gap-3 p-3 rounded-lg bg-background/50 border border-border/20">
              <Terminal className="h-4.5 w-4.5 text-primary shrink-0 mt-0.5" />
              <div className="flex flex-col gap-0.5">
                <span className="font-bold text-foreground">Local-First Vector Compute</span>
                <p className="text-muted-foreground leading-relaxed text-[11px]">
                  Keep user data local. Embedding models and vector stores should remain fully self-hostable to guarantee privacy.
                </p>
              </div>
            </div>

            {/* Value 2 */}
            <div className="flex items-start gap-3 p-3 rounded-lg bg-background/50 border border-border/20">
              <Lightbulb className="h-4.5 w-4.5 text-primary shrink-0 mt-0.5" />
              <div className="flex flex-col gap-0.5">
                <span className="font-bold text-foreground">Open-Source Blueprints</span>
                <p className="text-muted-foreground leading-relaxed text-[11px]">
                  Show the errors, warnings, and migration blocks. Publishing full schema specifications builds collective developer trust.
                </p>
              </div>
            </div>

            {/* Value 3 */}
            <div className="flex items-start gap-3 p-3 rounded-lg bg-background/50 border border-border/20">
              <Compass className="h-4.5 w-4.5 text-primary shrink-0 mt-0.5" />
              <div className="flex flex-col gap-0.5">
                <span className="font-bold text-foreground">Cognitive Flow Design</span>
                <p className="text-muted-foreground leading-relaxed text-[11px]">
                  High information density combined with keyboard-first shortcuts and clean, responsive typography maximizes builder flow.
                </p>
              </div>
            </div>
          </div>
        </div>

      </section>

      {/* 3. TIMELINE SECTION */}
      <section className="flex flex-col gap-8 border-t border-border/40 pt-16">
        <div className="flex flex-col gap-1.5">
          <span className="font-mono text-[10px] tracking-[0.25em] text-primary/80 uppercase">
            {"// ARCHITECTURE MILESTONES"}
          </span>
          <h2 className="text-2xl font-bold tracking-tight text-foreground">
            Development Timeline
          </h2>
        </div>
        
        <div className="flex flex-col border-l border-border/40 pl-6 ml-3 gap-8">
          
          {/* Milestone 1 */}
          <div className="relative group">
            <span className="absolute -left-[29px] top-1.5 w-3 h-3 rounded-full bg-primary border-2 border-background shadow-[0_0_10px_rgba(59,130,246,0.5)] animate-pulse" />
            <div className="flex flex-col gap-1.5">
              <span className="font-mono text-[9px] text-primary/80 uppercase font-black">
                JULY 2026
              </span>
              <h4 className="font-bold text-foreground text-sm">
                BuildWithPNJ Command Center Launch
              </h4>
              <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed max-w-2xl">
                Released the unified dashboard, connecting live GitHub commits telemetry, weekly targets metrics, and local R&D experiments to public developers.
              </p>
            </div>
          </div>
          
          {/* Milestone 2 */}
          <div className="relative group">
            <span className="absolute -left-[29px] top-1.5 w-3 h-3 rounded-full bg-primary border-2 border-background" />
            <div className="flex flex-col gap-1.5">
              <span className="font-mono text-[9px] text-muted-foreground/80 uppercase font-bold">
                MAY 2026
              </span>
              <h4 className="font-bold text-foreground text-sm">
                Warborn OS Core Alpha Shipped
              </h4>
              <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed max-w-2xl">
                Deployed a secure, self-hosted workspace instance containing double-entry ledgers, automated habits checking, and Google Drive metadata folder sync.
              </p>
            </div>
          </div>

          {/* Milestone 3 */}
          <div className="relative group">
            <span className="absolute -left-[29px] top-1.5 w-3 h-3 rounded-full bg-primary border-2 border-background" />
            <div className="flex flex-col gap-1.5">
              <span className="font-mono text-[9px] text-muted-foreground/80 uppercase font-bold">
                JANUARY 2026
              </span>
              <h4 className="font-bold text-foreground text-sm">
                AI Orchestration R&D Init
              </h4>
              <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed max-w-2xl">
                Conducted consensus protocol evaluations inside LangGraph and custom state machines to minimize logic loop errors in multi-agent routing systems.
              </p>
            </div>
          </div>

        </div>
      </section>

      {/* 4. CURRENT TARGETS SECTION */}
      <section className="flex flex-col gap-8 border-t border-border/40 pt-16">
        <div className="flex flex-col gap-1.5">
          <span className="font-mono text-[10px] tracking-[0.25em] text-primary/80 uppercase">
            {"// ROADMAP MATRIX"}
          </span>
          <h2 className="text-2xl font-bold tracking-tight text-foreground">
            Current Target Objectives
          </h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-[11px] font-mono">
          {/* Target 1 */}
          <div className="p-4 rounded-xl border border-border/40 bg-card/25 backdrop-blur-sm flex items-center justify-between gap-4 shadow-sm hover:border-primary/20 transition-all">
            <div className="flex items-center gap-3 text-muted-foreground">
              <CheckCircle2 className="h-4.5 w-4.5 text-emerald-400 shrink-0" />
              <span>Launch Personal OS v1.0 Container</span>
            </div>
            <span className="text-emerald-400 font-bold px-1.5 py-0.5 rounded bg-emerald-500/5 border border-emerald-500/10 text-[9px]">
              [ COMPLETED ]
            </span>
          </div>

          {/* Target 2 */}
          <div className="p-4 rounded-xl border border-border/40 bg-card/25 backdrop-blur-sm flex items-center justify-between gap-4 shadow-sm hover:border-primary/20 transition-all">
            <div className="flex items-center gap-3 text-muted-foreground">
              <CheckCircle2 className="h-4.5 w-4.5 text-emerald-400 shrink-0" />
              <span>Publish 5 Systems Architecture Log files</span>
            </div>
            <span className="text-emerald-400 font-bold px-1.5 py-0.5 rounded bg-emerald-500/5 border border-emerald-500/10 text-[9px]">
              [ COMPLETED ]
            </span>
          </div>

          {/* Target 3 */}
          <div className="p-4 rounded-xl border border-border/40 bg-card/25 backdrop-blur-sm flex items-center justify-between gap-4 shadow-sm hover:border-primary/20 transition-all">
            <div className="flex items-center gap-3 text-muted-foreground">
              <Circle className="h-4.5 w-4.5 text-primary shrink-0" />
              <span>Ship Experiment-002: Voice Personal OS</span>
            </div>
            <span className="text-primary font-bold px-1.5 py-0.5 rounded bg-primary/5 border border-primary/10 text-[9px]">
              [ IN_PROGRESS ]
            </span>
          </div>

          {/* Target 4 */}
          <div className="p-4 rounded-xl border border-border/40 bg-card/25 backdrop-blur-sm flex items-center justify-between gap-4 shadow-sm hover:border-primary/20 transition-all">
            <div className="flex items-center gap-3 text-muted-foreground">
              <Circle className="h-4.5 w-4.5 text-primary shrink-0" />
              <span>Grow local newsletter crew to 1K subscribers</span>
            </div>
            <span className="text-primary font-bold px-1.5 py-0.5 rounded bg-primary/5 border border-primary/10 text-[9px]">
              [ IN_PROGRESS ]
            </span>
          </div>
        </div>
      </section>

      {/* Footer Call-To-Action */}
      <div className="flex justify-center border-t border-border/40 pt-12">
        <Link 
          href="/contact" 
          className="inline-flex items-center gap-2 h-12 px-6 rounded-xl font-medium bg-primary text-primary-foreground hover:opacity-90 shadow-md shadow-primary/20 transition-all active:scale-[0.98]"
        >
          {"Initiate Connection"} <ArrowRight className="h-4 w-4" />
        </Link>
      </div>

    </div>
  );
}
