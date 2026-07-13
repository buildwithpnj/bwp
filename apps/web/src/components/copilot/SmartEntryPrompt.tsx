'use client';

interface SmartEntryPromptProps {
  intent: string;
  onAccept: () => void;
}

export function SmartEntryPrompt({ intent, onAccept }: SmartEntryPromptProps) {
  if (intent !== 'stuck' && intent !== 'reviewing') return null;
  return (
    <div className="bg-primary/5 border border-primary/20 p-3 rounded-lg text-left space-y-2">
      <h4 className="font-semibold text-xs text-foreground">Proactive Presence Help</h4>
      <p className="text-[10px] text-muted-foreground leading-normal">
        {intent === 'stuck'
          ? 'Would you like the copilot to walk you through the diagnostics report and suggest recovery options?'
          : 'Would you like the copilot to compile a quick checkpoint status review for this objective?'}
      </p>
      <button
        onClick={onAccept}
        className="bg-primary text-primary-foreground px-2.5 py-1 rounded text-[10px] font-medium hover:bg-primary/95 transition-all"
      >
        Get Help
      </button>
    </div>
  );
}
