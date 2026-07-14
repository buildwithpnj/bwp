'use client';

import React, { useState } from 'react';
import { Terminal, Send, Layers, Database, Sparkles, Check, Play } from 'lucide-react';

export default function WorkspacePage() {
  const [prompt, setPrompt] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [outputs, setOutputs] = useState({
    gpt4: '',
    claude3: '',
    gemini15: ''
  });
  const [injectedContext, setInjectedContext] = useState<string | null>(null);

  const handleRunArena = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || isSubmitting) return;

    setIsSubmitting(true);
    // Simulate multi-model streaming responses
    setTimeout(() => {
      setOutputs({
        gpt4: `// GPT-4o EXECUTION RESPONSE\nconst apiGateway = new Router();\n\napiGateway.use(async (ctx, next) => {\n  const token = ctx.headers['x-gating-token'];\n  if (!verifyGatingToken(token)) {\n    ctx.status = 401;\n    ctx.body = { error: 'GATING_REJECTED' };\n    return;\n  }\n  await next();\n});`,
        claude3: `// Claude 3.5 Sonnet Response (Optimized Security)\nimport { verifyToken } from '@personal-os/gate';\n\nexport const gatingMiddleware = async (req, res, next) => {\n  try {\n    const token = req.headers['x-gating-token'];\n    const isValid = await verifyToken(token);\n    if (!isValid) {\n      return res.status(401).json({ status: 'denied', reason: 'GATE_LOCKED' });\n    }\n    next();\n  } catch (err) {\n    next(err);\n  }\n};`,
        gemini15: `// Gemini 1.5 Pro Response (High Context Fit)\n// Verified Gating Layer for Web Sockets & HTTP\nconst checkGate = (token) => {\n  if (token === process.env.SYSTEM_GATING_KEY) {\n    return true;\n  }\n  throw new Error('UNAUTHORIZED_OS_GATE');\n};`
      });
      setIsSubmitting(false);
    }, 1500);
  };

  return (
    <div className="space-y-6 animate-fade-in text-pnj-textStrong font-sans">
      {/* Page Header */}
      <div className="flex items-center justify-between border-b border-border pb-3">
        <div>
          <span className="font-mono text-[10px] tracking-[0.25em] text-primary uppercase font-bold">SYSTEM_FORGE // MULTI_MODEL_ARENA</span>
          <h1 className="text-xl font-bold tracking-tight mt-0.5">THE FORGE</h1>
        </div>
        <div className="flex items-center gap-2 font-mono text-[11px]">
          <span className="text-muted-foreground">MODELS: 3 ACTIVE</span>
          <span className="opacity-30">|</span>
          <span className="text-emerald-400">STATUS: READY</span>
        </div>
      </div>

      {/* Context Injector & Input Strip */}
      <div className="border border-border bg-card p-4 space-y-3 font-mono">
        <div className="flex items-center justify-between text-xs border-b border-border/40 pb-2">
          <span className="text-[10px] text-muted-foreground uppercase font-bold">CONTEXT_INJECTOR</span>
          <div className="flex gap-2">
            <button 
              onClick={() => setInjectedContext(injectedContext === 'cortex' ? null : 'cortex')}
              className={`px-2 py-0.5 text-[9px] uppercase border transition-colors ${injectedContext === 'cortex' ? 'text-primary border-primary bg-primary/5' : 'text-muted-foreground border-border hover:border-muted-foreground'}`}
            >
              {injectedContext === 'cortex' ? '[X] Cortex Notes Injected' : '+ Inject Cortex Notes'}
            </button>
            <button 
              onClick={() => setInjectedContext(injectedContext === 'missions' ? null : 'missions')}
              className={`px-2 py-0.5 text-[9px] uppercase border transition-colors ${injectedContext === 'missions' ? 'text-primary border-primary bg-primary/5' : 'text-muted-foreground border-border hover:border-muted-foreground'}`}
            >
              {injectedContext === 'missions' ? '[X] Missions Synced' : '+ Inject Active Missions'}
            </button>
          </div>
        </div>

        <form onSubmit={handleRunArena} className="flex gap-2 bg-background border border-border/60 px-3 py-2">
          <span className="text-primary font-bold mr-1 self-center">&gt;</span>
          <input
            type="text"
            placeholder="PROMPT THE LLM ARENA TO COMPILE COMPARATIVE CODE OR DESIGNS..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={isSubmitting}
            className="flex-1 bg-transparent outline-none border-none text-foreground placeholder:text-muted-foreground uppercase tracking-wide font-mono text-[11px]"
          />
          <button
            type="submit"
            disabled={isSubmitting || !prompt.trim()}
            className="px-4 py-1 bg-primary text-primary-foreground font-mono text-3xs font-bold uppercase tracking-wider hover:bg-primary/95 disabled:opacity-30 transition-opacity flex items-center gap-1.5"
          >
            {isSubmitting ? 'RUNNING...' : <>RUN <Play className="h-3 w-3 fill-current" /></>}
          </button>
        </form>
      </div>

      {/* Split-pane Arena Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-3 border border-border bg-card divide-y lg:divide-y-0 lg:divide-x divide-border/60">
        
        {/* Model 1: GPT-4o */}
        <div className="p-4 flex flex-col justify-between min-h-[380px]">
          <div>
            <div className="flex items-center justify-between border-b border-border/40 pb-2 mb-3">
              <span className="text-[10px] font-mono text-muted-foreground uppercase font-bold">01 // GPT_4O_MINI</span>
              <span className="text-[9px] font-mono text-sky-400 bg-sky-500/10 px-1.5 py-0.5 border border-sky-500/20">SPEED_PRIORITY</span>
            </div>
            
            {isSubmitting && !outputs.gpt4 ? (
              <div className="space-y-2 py-4 animate-pulse font-mono text-[10px] text-muted-foreground">
                <div className="h-2.5 bg-muted/20 w-3/4" />
                <div className="h-2.5 bg-muted/20 w-1/2" />
                <div className="h-2.5 bg-muted/20 w-2/3" />
              </div>
            ) : outputs.gpt4 ? (
              <pre className="font-mono text-[10px] text-muted-foreground bg-muted/5 p-3 border border-border/40 whitespace-pre overflow-x-auto leading-relaxed">
                <code>{outputs.gpt4}</code>
              </pre>
            ) : (
              <p className="text-3xs text-muted-foreground italic font-mono py-4">Awaiting arena prompt execution...</p>
            )}
          </div>
          <div className="mt-4 pt-3 border-t border-border/40 text-[9px] font-mono text-muted-foreground flex justify-between">
            <span>TOKENS: 452</span>
            <span>LATENCY: 420ms</span>
          </div>
        </div>

        {/* Model 2: Claude 3.5 Sonnet */}
        <div className="p-4 flex flex-col justify-between min-h-[380px]">
          <div>
            <div className="flex items-center justify-between border-b border-border/40 pb-2 mb-3">
              <span className="text-[10px] font-mono text-muted-foreground uppercase font-bold">02 // CLAUDE_35_SONNET</span>
              <span className="text-[9px] font-mono text-primary bg-primary/10 px-1.5 py-0.5 border border-primary/20">CODE_QUALITY</span>
            </div>

            {isSubmitting && !outputs.claude3 ? (
              <div className="space-y-2 py-4 animate-pulse font-mono text-[10px] text-muted-foreground">
                <div className="h-2.5 bg-muted/20 w-3/4" />
                <div className="h-2.5 bg-muted/20 w-1/2" />
                <div className="h-2.5 bg-muted/20 w-2/3" />
              </div>
            ) : outputs.claude3 ? (
              <pre className="font-mono text-[10px] text-muted-foreground bg-muted/5 p-3 border border-border/40 whitespace-pre overflow-x-auto leading-relaxed">
                <code>{outputs.claude3}</code>
              </pre>
            ) : (
              <p className="text-3xs text-muted-foreground italic font-mono py-4">Awaiting arena prompt execution...</p>
            )}
          </div>
          <div className="mt-4 pt-3 border-t border-border/40 text-[9px] font-mono text-muted-foreground flex justify-between">
            <span>TOKENS: 612</span>
            <span>LATENCY: 850ms</span>
          </div>
        </div>

        {/* Model 3: Gemini 1.5 Pro */}
        <div className="p-4 flex flex-col justify-between min-h-[380px]">
          <div>
            <div className="flex items-center justify-between border-b border-border/40 pb-2 mb-3">
              <span className="text-[10px] font-mono text-muted-foreground uppercase font-bold">03 // GEMINI_15_PRO</span>
              <span className="text-[9px] font-mono text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 border border-emerald-500/20">HIGH_CONTEXT</span>
            </div>

            {isSubmitting && !outputs.gemini15 ? (
              <div className="space-y-2 py-4 animate-pulse font-mono text-[10px] text-muted-foreground">
                <div className="h-2.5 bg-muted/20 w-3/4" />
                <div className="h-2.5 bg-muted/20 w-1/2" />
                <div className="h-2.5 bg-muted/20 w-2/3" />
              </div>
            ) : outputs.gemini15 ? (
              <pre className="font-mono text-[10px] text-muted-foreground bg-muted/5 p-3 border border-border/40 whitespace-pre overflow-x-auto leading-relaxed">
                <code>{outputs.gemini15}</code>
              </pre>
            ) : (
              <p className="text-3xs text-muted-foreground italic font-mono py-4">Awaiting arena prompt execution...</p>
            )}
          </div>
          <div className="mt-4 pt-3 border-t border-border/40 text-[9px] font-mono text-muted-foreground flex justify-between">
            <span>TOKENS: 580</span>
            <span>LATENCY: 910ms</span>
          </div>
        </div>

      </div>
    </div>
  );
}
