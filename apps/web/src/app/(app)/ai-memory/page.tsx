'use client';

import { Cpu, Brain, Network, Compass, Activity, FileText } from 'lucide-react';

export default function AiMemoryPage() {
  return (
    <div className="space-y-6 animate-fade-in text-foreground">
      {/* System Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">Embedding Database</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <Brain className="h-7 w-7 text-primary" />
            AI Memory & Context
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Vectorized cognitive memory highlights, context windows, and user preferences log.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* Core telemetry */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Activity className="h-4 w-4 text-primary" />
            Vector Dimensions
          </h3>
          <div className="space-y-3 font-mono text-2xs">
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span className="text-muted-foreground">Embedding Model:</span>
              <span className="text-foreground">text-embedding-3-small</span>
            </div>
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span className="text-muted-foreground">Dimensions:</span>
              <span className="text-foreground">1536</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Total Vectors:</span>
              <span className="text-foreground">4,192 nodes</span>
            </div>
          </div>
        </div>

        {/* Recent cognitive memories */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4 col-span-2">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Compass className="h-4 w-4 text-primary" />
            Cognitive Recall Logs
          </h3>
          <div className="space-y-3 text-xs">
            {[
              { text: '"User preferences highlight OAuth project target: Drive A for primary files, Drive B for media/images, and fallback routing active on exceptions."', date: '10 mins ago' },
              { text: '"User prefers Postgres-compliant sync migrations over threading blocks on uvicorn reloads."', date: '2 hours ago' },
            ].map((node, idx) => (
              <div key={idx} className="p-3 rounded-xl border border-border/60 bg-muted/20 space-y-1">
                <p className="text-foreground leading-relaxed italic">{node.text}</p>
                <span className="text-3xs text-muted-foreground font-mono block text-right mt-1">{node.date}</span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
