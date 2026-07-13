import React from 'react';

interface ActionResultCardProps {
  content: string;
}

export function ActionResultCard({ content }: ActionResultCardProps) {
  // Parse the fields from the structured response
  const lines = content.split('\n');
  const fields: { [key: string]: string } = {};

  lines.forEach(line => {
    const idx = line.indexOf(':');
    if (idx !== -1) {
      const key = line.substring(0, idx).trim().toLowerCase();
      const val = line.substring(idx + 1).trim();
      fields[key] = val;
    }
  });

  const status = fields['status'] || 'Unknown';
  const action = fields['action'] || 'Action';
  const result = fields['result'] || '';
  const scope = fields['scope'] || 'workspace';
  const next = fields['next'] || '';

  // Classify styles based on status
  let statusColor = 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20';
  let badgeColor = 'bg-emerald-500 text-emerald-950';
  
  if (status.toLowerCase().includes('fail')) {
    statusColor = 'text-rose-500 bg-rose-500/10 border-rose-500/20';
    badgeColor = 'bg-rose-500 text-rose-950';
  } else if (status.toLowerCase().includes('block')) {
    statusColor = 'text-amber-500 bg-amber-500/10 border-amber-500/20';
    badgeColor = 'bg-amber-500 text-amber-950';
  } else if (status.toLowerCase().includes('confirm')) {
    statusColor = 'text-indigo-500 bg-indigo-500/10 border-indigo-500/20';
    badgeColor = 'bg-indigo-500 text-indigo-950';
  } else if (status.toLowerCase().includes('queue')) {
    statusColor = 'text-sky-500 bg-sky-500/10 border-sky-500/20';
    badgeColor = 'bg-sky-500 text-sky-950';
  }

  return (
    <div className={`p-3 rounded-lg border flex flex-col gap-2 ${statusColor} text-[11px] font-sans transition-all duration-200 hover:scale-[1.01]`}>
      <div className="flex items-center justify-between border-b border-white/5 pb-1">
        <span className="font-bold tracking-wide uppercase text-[9px] opacity-90">{action}</span>
        <span className={`px-1.5 py-0.5 rounded text-[8px] font-bold tracking-wider uppercase ${badgeColor}`}>
          {status}
        </span>
      </div>
      <div className="text-foreground opacity-90 font-medium whitespace-pre-wrap leading-relaxed">
        {result}
      </div>
      <div className="flex items-center justify-between text-[9px] opacity-70 mt-1">
        <span>Scope: {scope}</span>
        {next && <span className="font-semibold underline decoration-dotted cursor-pointer">Next: {next}</span>}
      </div>
    </div>
  );
}

export function isStructuredResponse(content: string): boolean {
  return content.includes('Status:') && content.includes('Action:') && content.includes('Result:');
}
