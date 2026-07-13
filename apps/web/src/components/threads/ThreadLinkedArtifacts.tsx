'use client';

interface ThreadLinkedArtifactsProps {
  links: Array<{ type: string; id: string }>;
}

export function ThreadLinkedArtifacts({ links }: ThreadLinkedArtifactsProps) {
  if (links.length === 0) return null;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-[9px] text-muted-foreground uppercase">Linked Runs:</span>
      <div className="flex flex-wrap gap-1.5">
        {links.map((link, idx) => (
          <span
            key={idx}
            className="bg-muted text-muted-foreground px-2 py-0.5 rounded text-[10px] border border-border"
          >
            {link.type}: {link.id}
          </span>
        ))}
      </div>
    </div>
  );
}
