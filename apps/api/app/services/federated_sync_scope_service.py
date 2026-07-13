from typing import List

class FederatedSyncScopeService:
    @classmethod
    def filter_targets(cls, nodes: List[str], tenant_ids: List[str]) -> List[dict]:
        """
        Builds sync scope lists based on target nodes/tenants.
        """
        targets = []
        for node in nodes:
            for tenant in tenant_ids:
                targets.append({"node_ip": node, "tenant_id": tenant})
        return targets
        
    @classmethod
    def classify_severity(cls, diff: dict) -> str:
        """
        Classifies risk limits.
        """
        if len(diff) > 3 or any("limit" in k for k in diff.keys()):
            return "high"
        return "low"
