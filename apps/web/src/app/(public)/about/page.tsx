import React from 'react';
import Link from 'next/link';
import { ArrowRight, Terminal, Lightbulb, Compass } from 'lucide-react';

export const metadata = {
  title: 'About — BuildWithPNJ',
  description: 'Prakash Nandan Jha (PNJ), AI Engineer building production-ready tools in public. Read about my origin story, values, and targets.',
};

export default function PublicAboutPage() {
  return (
    <div className="flex flex-col gap-12 md:gap-16">
      
      {/* 1. PROFILE / HEADER */}
      <section className="flex flex-col md:flex-row items-start gap-8 border-b border-border pb-10">
        {/* Profile Circle Avatar */}
        <div className="w-24 h-24 sm:w-28 sm:h-28 rounded-full border border-border bg-card flex items-center justify-center font-pixel text-4xl text-primary shrink-0 select-none">
          PNJ
        </div>

        <div className="flex flex-col gap-3 text-left">
          <div className="font-pixel text-[11px] text-primary tracking-wider uppercase">{"// ENGINEER ORIGIN"}</div>
          <h1 className="text-3xl sm:text-4xl font-pixel text-foreground">{"Hey, I'm Prakash 👋"}</h1>
          <p className="text-base sm:text-lg text-muted-foreground max-w-2xl leading-relaxed">
            AI Engineer building production-grade, self-hostable tools in public. I map vector databases, configure multi-agent frameworks, and deploy codebases from the ground up.
          </p>
        </div>
      </section>

      {/* 2. THE STORY */}
      <section className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 text-left">
        <div className="lg:col-span-8 flex flex-col gap-6">
          <h2 className="font-pixel text-xl text-foreground tracking-tight uppercase">{"// MY STORY"}</h2>
          
          <div className="text-sm text-foreground leading-relaxed flex flex-col gap-4">
            <p>
              I got into programming because I wanted to solve my own problems. Initially, this meant coding simple command-line scripts to automate backups or manage files. As local language models emerged, I realized that developers had a once-in-a-generation opportunity to create custom intelligence engines.
            </p>
            <p>
              But there was a gap. Most tutorials stopped at simple notebook scripts or toy chat interfaces. They hid the messy reality of async database queues, rate limiting, context window leaks, and production migrations.
            </p>
            <p>
              {"That's why I created"} **BuildWithPNJ**. {"It represents a commitment to building real, self-hostable software that solves daily operational needs—and documenting every architecture trade-off along the way."}
            </p>
          </div>
        </div>

        {/* Philosophy sidebar */}
        <div className="lg:col-span-4 p-5 rounded-2xl border border-border bg-card flex flex-col gap-4 h-fit">
          <h3 className="font-pixel text-xs text-foreground uppercase tracking-wider">{"// CORE VALUES"}</h3>
          
          <div className="flex flex-col gap-3 text-xs text-muted-foreground leading-relaxed">
            <div className="flex items-start gap-3">
              <Terminal className="h-4 w-4 text-primary shrink-0 mt-0.5" />
              <div>
                <strong className="text-foreground">Run Locally:</strong> Keep user data local. Vector indexes and databases should remain self-hostable.
              </div>
            </div>
            <div className="flex items-start gap-3">
              <Lightbulb className="h-4 w-4 text-primary shrink-0 mt-0.5" />
              <div>
                <strong className="text-foreground">Iterate in the Open:</strong> Show the errors, the warnings, and the refactoring blocks. Transparent code builds trust.
              </div>
            </div>
            <div className="flex items-start gap-3">
              <Compass className="h-4 w-4 text-primary shrink-0 mt-0.5" />
              <div>
                <strong className="text-foreground">Frictionless UX:</strong> High performance and clean layouts improve developers&apos; cognitive flow.
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. TIMELINE */}
      <section className="flex flex-col gap-6 border-t border-border pt-10 text-left">
        <h2 className="font-pixel text-xl text-foreground tracking-tight uppercase">{"// MILESTONES"}</h2>
        
        <div className="flex flex-col border-l border-border pl-4 ml-2">
          
          <div className="relative py-4 group">
            <span className="absolute -left-[21px] top-6 w-2.5 h-2.5 rounded-full bg-primary border border-primary/20 shadow-[0_0_10px_rgba(59,130,246,0.4)]" />
            <span className="text-[10px] font-mono text-muted-foreground">JULY 2026</span>
            <h4 className="font-bold text-foreground text-sm mt-0.5">BuildWithPNJ Digital HQ Launch</h4>
            <p className="text-xs text-muted-foreground mt-1 leading-relaxed max-w-xl">
              Released this website containing our unified projects, journal, and real-time command telemetry to public developers.
            </p>
          </div>
          
          <div className="relative py-4 group">
            <span className="absolute -left-[21px] top-6 w-2.5 h-2.5 rounded-full bg-primary" />
            <span className="text-[10px] font-mono text-muted-foreground">MAY 2026</span>
            <h4 className="font-bold text-foreground text-sm mt-0.5">Personal OS Alpha Shipped</h4>
            <p className="text-xs text-muted-foreground mt-1 leading-relaxed max-w-xl">
              Deployed a self-hosted personal Operating System container with double-entry ledgers, habit logs, and local vector notes storage.
            </p>
          </div>

          <div className="relative py-4 group">
            <span className="absolute -left-[21px] top-6 w-2.5 h-2.5 rounded-full bg-primary" />
            <span className="text-[10px] font-mono text-muted-foreground">JANUARY 2026</span>
            <h4 className="font-bold text-foreground text-sm mt-0.5">AI Orchestration R&D</h4>
            <p className="text-xs text-muted-foreground mt-1 leading-relaxed max-w-xl">
              Evaluated multi-agent systems inside LangGraph, mapping consensus protocols to minimize logical failures in code reviewers.
            </p>
          </div>

        </div>
      </section>

      {/* 4. CURRENT GOALS */}
      <section className="flex flex-col gap-6 border-t border-border pt-10 text-left">
        <h2 className="font-pixel text-xl text-foreground tracking-tight uppercase">{"// CURRENT TARGETS"}</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono text-muted-foreground">
          <div className="p-4 rounded-xl border border-border bg-card flex items-center gap-3">
            <span className="text-positive font-bold">☑</span>
            <span>Launch Personal OS v1.0 Container</span>
          </div>
          <div className="p-4 rounded-xl border border-border bg-card flex items-center gap-3">
            <span className="text-positive font-bold">☑</span>
            <span>Publish 5 Systems Architecture Log files</span>
          </div>
          <div className="p-4 rounded-xl border border-border bg-card flex items-center gap-3">
            <span className="text-primary font-bold">☐</span>
            <span>Ship Experiment-002: Voice Personal OS</span>
          </div>
          <div className="p-4 rounded-xl border border-border bg-card flex items-center gap-3">
            <span className="text-primary font-bold">☐</span>
            <span>Grow local newsletter crew to 1K subscribers</span>
          </div>
        </div>
      </section>

      {/* Footer CTA */}
      <div className="flex justify-center mt-6">
        <Link 
          href="/contact" 
          className="inline-flex items-center gap-2 h-12 px-6 rounded-xl font-medium bg-primary text-primary-foreground hover:opacity-90 shadow-md shadow-primary/20 transition-all active:scale-[0.98]"
        >
          {"Let's Connect"} <ArrowRight className="h-4 w-4" />
        </Link>
      </div>

    </div>
  );
}
