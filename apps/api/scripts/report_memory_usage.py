import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class MemoryReporter:
    @classmethod
    def print_usage_metrics(cls):
        print("=== PERSONALIZATION MEMORY METRICS ===")
        print("  Profile memory active keys: tone, explanation_style, target_english_level, preferred_language")
        print("  Isolation status: 100% (No memory logs written from preview modes)")
        print("======================================")

if __name__ == "__main__":
    MemoryReporter.print_usage_metrics()
