from app.services.document_graph_service import DocumentGraphService

def test_add_nodes_and_edges():
    DocumentGraphService.add_node("c1", "tenant_1", "chunk")
    DocumentGraphService.add_node("c2", "tenant_1", "chunk")
    DocumentGraphService.add_edge("c1", "c2", "tenant_1", "references")
    
    adjs = DocumentGraphService.get_adjacencies("c1", "tenant_1")
    assert len(adjs) == 1
    assert adjs[0]["relationship"] == "references"
