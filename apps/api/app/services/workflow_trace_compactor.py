from typing import List, Dict, Any

class WorkflowTraceCompactor:
    @classmethod
    def compact_traces(cls, traces: List[Dict[str, Any]]) -> str:
        """
        Compresses trace lists into a single consolidated text summary.
        """
        if not traces:
            return "No prior traces."
        summaries = []
        for idx, t in enumerate(traces):
            summaries.append(f"Run {t.get('id', idx)}: {t.get('status', 'unknown')} ({len(t.get('steps', []))} steps)")
        return " | ".join(summaries)
