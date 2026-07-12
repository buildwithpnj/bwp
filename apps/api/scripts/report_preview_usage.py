import sys
import os

# Append project path to load app packages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.preview_analytics_service import PreviewAnalyticsService

def main():
    metrics = PreviewAnalyticsService.get_metrics()
    print("=== WARBORN PUBLIC PREVIEW USAGE REPORT ===")
    print(f"Total Preview Sessions: {metrics['preview_starts']}")
    print(f"Total Preview Turns: {metrics['preview_turns']}")
    print(f"Blocked Abuse Attempts: {metrics['blocked_abuse_attempts']}")
    print(f"Total Tokens Consumed: {metrics['total_tokens_consumed']}")
    print(f"Total Cost (USD): ${metrics['total_cost_usd']:.4f}")
    print(f"Average Cost Per Session: ${metrics['average_cost_per_session_usd']:.6f}")
    print("===========================================")

if __name__ == "__main__":
    main()
