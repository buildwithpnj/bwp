from typing import List, Dict

class CrossTenantAnalyticsService:
    @classmethod
    def aggregate_anonymous_metrics(cls, tenant_metrics: List[Dict[str, float]]) -> float:
        """
        Aggregates metadata pattern statistics without disclosing client variables.
        """
        if not tenant_metrics:
            return 0.0
        return sum(m.get("failure_rate", 0.0) for m in tenant_metrics) / len(tenant_metrics)
