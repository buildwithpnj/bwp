from typing import List, Dict, Any

class DocumentGraphService:
    _nodes: Dict[str, Dict[str, Any]] = {}
    _edges: List[Dict[str, Any]] = []

    @classmethod
    def add_node(cls, node_id: str, tenant_id: str, label: str, properties: Dict[str, Any] = None) -> None:
        """
        Registers a document, chunk, or entity node inside the graph.
        """
        cls._nodes[node_id] = {
            "id": node_id,
            "tenant_id": tenant_id,
            "label": label,
            "properties": properties or {}
        }

    @classmethod
    def add_edge(cls, source_id: str, target_id: str, tenant_id: str, relationship: str) -> None:
        """
        Establishes a directed link between nodes.
        """
        cls._edges.append({
            "source": source_id,
            "target": target_id,
            "tenant_id": tenant_id,
            "relationship": relationship
        })

    @classmethod
    def get_adjacencies(cls, node_id: str, tenant_id: str) -> List[Dict[str, Any]]:
        """
        Returns adjacent edges inside the tenant boundary.
        """
        return [
            e for e in cls._edges
            if e["tenant_id"] == tenant_id and (e["source"] == node_id or e["target"] == node_id)
        ]
