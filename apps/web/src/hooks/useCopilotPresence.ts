import { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';

export interface PresenceConfig {
  intent: 'stuck' | 'executing' | 'reviewing' | 'browsing';
  directive: 'stay_silent' | 'suggest_recovery' | 'summarize' | 'ask_open_ended';
  should_show_hint: boolean;
}

export function useCopilotPresence() {
  const pathname = usePathname();
  const [presence, setPresence] = useState<PresenceConfig>({
    intent: 'browsing',
    directive: 'ask_open_ended',
    should_show_hint: true
  });
  const [suggestions, setSuggestions] = useState<string[]>([]);

  const fetchPresence = async () => {
    try {
      // Direct client-side presence evaluation logic to preserve budget and performance
      const route = pathname || '/';
      const isStuck = route.includes('diagnostics') || route.includes('recovery');
      const isExec = route.includes('workspace') || route.includes('tools');
      const isReview = route.includes('objectives');

      const intent = isStuck ? 'stuck' : isExec ? 'executing' : isReview ? 'reviewing' : 'browsing';
      const directive = isStuck
        ? 'suggest_recovery'
        : isExec
        ? 'stay_silent'
        : isReview
        ? 'summarize'
        : 'ask_open_ended';

      setPresence({
        intent,
        directive,
        should_show_hint: directive !== 'stay_silent'
      });

      // Context suggestions mapping
      if (intent === 'stuck') {
        setSuggestions(['Explain last error', 'Show recovery suggestions']);
      } else if (intent === 'executing') {
        setSuggestions(['Show active tasks', 'Pause workflow']);
      } else if (intent === 'reviewing') {
        setSuggestions(['Verify current checkpoint', 'Generate progress summary']);
      } else {
        setSuggestions(['Check Active Tasks', 'View Telemetry']);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchPresence();
  }, [pathname]);

  return { presence, suggestions };
}
