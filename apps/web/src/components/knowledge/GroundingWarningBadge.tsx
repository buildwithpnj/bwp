'use client';

interface GroundingWarningBadgeProps {
  score: number;
}

export function GroundingWarningBadge({ score }: GroundingWarningBadgeProps) {
  const isWeak = score < 0.6;
  return (
    <span
      className={`px-2.5 py-0.5 rounded-full text-[9px] font-semibold tracking-wide ${
        isWeak
          ? 'bg-rose-500/20 text-rose-400 border border-rose-500/20'
          : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/20'
      }`}
    >
      {isWeak ? 'Ungrounded Claims Risk' : 'Grounded Claims verified'}
    </span>
  );
}
export default GroundingWarningBadge;
