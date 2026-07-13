from app.services.document_graph_service import DocumentGraphService
from app.services.graph_retrieval_service import GraphRetrievalService

def test_traverse_graph():
    DocumentGraphService.add_node("c10", "tenant_1", "chunk")
    DocumentGraphService.add_node("c11", "tenant_1", "chunk")
    DocumentGraphService.add_edge("c10", "c11", "tenant_1", "related")
    
    results = GraphRetrievalService.traverse_graph(["c10"], "tenant_1", max_depth=2)
    assert "c11" in results
