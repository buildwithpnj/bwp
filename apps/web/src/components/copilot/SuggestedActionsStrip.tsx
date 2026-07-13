'use client';

interface SuggestedActionsStripProps {
  suggestions: string[];
  onSelectSuggestion: (text: string) => void;
}

export function SuggestedActionsStrip({
  suggestions,
  onSelectSuggestion
}: SuggestedActionsStripProps) {
  if (suggestions.length === 0) return null;
  return (
    <div className="flex flex-wrap gap-1.5 pt-1">
      {suggestions.map((s, idx) => (
        <button
          key={idx}
          type="button"
          onClick={() => onSelectSuggestion(s)}
          className="bg-muted hover:bg-accent border border-border text-[10px] text-foreground px-2 py-0.5 rounded transition-all duration-200"
        >
          {s}
        </button>
      ))}
    </div>
  );
}
