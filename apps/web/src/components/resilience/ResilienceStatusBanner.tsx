'use client';

interface ResilienceStatusBannerProps {
  level: string;
}

export function ResilienceStatusBanner({ level }: ResilienceStatusBannerProps) {
  const isNormal = level === 'normal';
  return (
    <div
      className={`border px-4 py-2.5 rounded-xl text-xs flex justify-between items-center transition-all ${
        isNormal
          ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
          : 'bg-rose-500/10 border-rose-500/20 text-rose-400'
      }`}
    >
      <div className="flex items-center gap-2">
        <span className={`w-1.5 h-1.5 rounded-full ${isNormal ? 'bg-emerald-400' : 'bg-rose-400 animate-pulse'}`} />
        <span>Resilience Status Level: <span className="font-bold uppercase">{level}</span></span>
      </div>
      <span className="text-[10px] opacity-80 font-mono">Self-Healing Enabled</span>
    </div>
  );
}
export default ResilienceStatusBanner;
