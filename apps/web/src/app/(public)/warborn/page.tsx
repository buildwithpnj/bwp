'use client';

import React from 'react';
import Link from 'next/link';
import { Shield, Sparkles, Key, Zap, CheckCircle2, ArrowRight } from 'lucide-react';

export default function WarbornLandingPage() {
  return (
    <div className="min-h-screen text-foreground relative grid-dots py-12 px-6 sm:px-12 flex flex-col items-center justify-center">
      {/* Hero Section */}
      <div className="max-w-4xl text-center space-y-6">
        <span className="text-3xs font-mono font-bold uppercase tracking-[0.3em] text-primary bg-primary/5 border border-primary/20 px-3 py-1 rounded-full">
          {"COGNITIVE OPERATING KERNEL"}
        </span>
        <h1 className="text-4xl sm:text-6xl font-black tracking-tight leading-none text-foreground">
          {"WARBORN SYSTEM"}
        </h1>
        <p className="text-sm sm:text-base text-muted-foreground max-w-2xl mx-auto leading-relaxed">
          {"Secure, private personal agent architecture designed for continuous workflow orchestration, language learning, and data synchronization."}
        </p>

        {/* CTA Actions */}
        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link
            href="/warborn/preview"
            className="h-10 px-6 rounded-xl bg-primary text-primary-foreground font-semibold hover:bg-primary/90 flex items-center gap-2 transition-all shadow-lg shadow-primary/10 text-xs"
          >
            {"Try Public Preview"} <Sparkles className="h-3.5 w-3.5" />
          </Link>
          <Link
            href="/login"
            className="h-10 px-6 rounded-xl border border-border/85 bg-card/45 hover:bg-muted/20 font-semibold flex items-center gap-2 transition-all text-xs"
          >
            {"Enter Dashboard"} <Key className="h-3.5 w-3.5" />
          </Link>
          <Link
            href="/request-access"
            className="h-10 px-6 rounded-xl border border-transparent text-primary hover:underline font-semibold flex items-center gap-1.5 transition-all text-xs"
          >
            {"Request Credentials"} <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>
      </div>

      {/* Capabilities */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mt-16 text-left">
        <div className="rounded-2xl border border-border/60 bg-card/25 p-6 space-y-4 hover:border-primary/20 transition-colors">
          <div className="h-10 w-10 rounded-xl bg-primary/10 border border-primary/25 flex items-center justify-center text-primary">
            <Shield className="h-5 w-5" />
          </div>
          <h3 className="text-sm font-bold text-foreground">{"Production Hardened"}</h3>
          <p className="text-xs text-muted-foreground leading-relaxed">
            {"Isolated sandbox runtimes protect internal memory models, preventing public preview loops from touching private OS credentials."}
          </p>
        </div>

        <div className="rounded-2xl border border-border/60 bg-card/25 p-6 space-y-4 hover:border-primary/20 transition-colors">
          <div className="h-10 w-10 rounded-xl bg-primary/10 border border-primary/25 flex items-center justify-center text-primary">
            <Zap className="h-5 w-5" />
          </div>
          <h3 className="text-sm font-bold text-foreground">{"Continuous Evaluation"}</h3>
          <p className="text-xs text-muted-foreground leading-relaxed">
            {"Leveraging an automated V8/V9 gold regression testing framework to maintain response quality, keeping latencies low."}
          </p>
        </div>

        <div className="rounded-2xl border border-border/60 bg-card/25 p-6 space-y-4 hover:border-primary/20 transition-colors">
          <div className="h-10 w-10 rounded-xl bg-primary/10 border border-primary/25 flex items-center justify-center text-primary">
            <Key className="h-5 w-5" />
          </div>
          <h3 className="text-sm font-bold text-foreground">{"Tenant Isolation"}</h3>
          <p className="text-xs text-muted-foreground leading-relaxed">
            {"Secure authenticated handoff transfers logged-in users to dedicated cloud modules with private knowledge stores."}
          </p>
        </div>
      </div>
    </div>
  );
}
