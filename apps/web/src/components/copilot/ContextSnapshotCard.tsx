'use client';

interface ContextSnapshotCardProps {
  intent: string;
}

export function ContextSnapshotCard({ intent }: ContextSnapshotCardProps) {
  return (
    <div className="bg-muted/40 border border-border p-2.5 rounded-md flex flex-col gap-1">
      <div className="flex items-center justify-between text-[9px] text-muted-foreground">
        <span>PRELOADED PERCEPTION CONTEXT</span>
        <span className="font-semibold text-primary">{intent.toUpperCase()}</span>
      </div>
      <p className="text-[10px] text-foreground leading-normal">
        Active metadata limits are validated and mapped for downstream safety checks.
      </p>
    </div>
  );
}
