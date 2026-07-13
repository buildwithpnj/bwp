from app.services.graph_expansion_policy import GraphExpansionPolicy

def test_expansion_bounds():
    assert GraphExpansionPolicy.should_expand("c1", 2) is True
    assert GraphExpansionPolicy.should_expand("c1", 4) is False
