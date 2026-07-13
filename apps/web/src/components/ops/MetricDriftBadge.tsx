'use client';

interface MetricDriftBadgeProps {
  value: number;
}

export function MetricDriftBadge({ value }: MetricDriftBadgeProps) {
  const isHigh = value > 75.0;
  return (
    <span
      className={`px-2 py-0.5 rounded-full text-[9px] font-semibold tracking-wide ${
        isHigh
          ? 'bg-rose-500/20 text-rose-400 border border-rose-500/20'
          : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/20'
      }`}
    >
      {isHigh ? 'High Drift Risk' : 'Normal'}
    </span>
  );
}
export default MetricDriftBadge;
