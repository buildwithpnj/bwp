from typing import List, Dict, Any
from app.services.document_graph_service import DocumentGraphService
from app.services.graph_expansion_policy import GraphExpansionPolicy

class GraphRetrievalService:
    @classmethod
    def traverse_graph(
        cls,
        seed_chunk_ids: List[str],
        tenant_id: str,
        max_depth: int = 2
    ) -> List[str]:
        """
        Performs bounded width/depth traversal of adjacent nodes.
        """
        visited = set(seed_chunk_ids)
        queue = [(cid, 0) for cid in seed_chunk_ids]
        
        while queue:
            current_id, depth = queue.pop(0)
            if depth >= max_depth:
                continue
                
            adjacencies = DocumentGraphService.get_adjacencies(current_id, tenant_id)
            for edge in adjacencies:
                neighbor = edge["target"] if edge["source"] == current_id else edge["source"]
                if neighbor not in visited:
                    if GraphExpansionPolicy.should_expand(neighbor, depth + 1):
                        visited.add(neighbor)
                        queue.append((neighbor, depth + 1))
                        
        return list(visited)
