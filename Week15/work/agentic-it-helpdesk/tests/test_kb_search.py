from src.tools.kb_search import kb_search

def test_kb_search_vpn():
    r = kb_search("vpn authentication failed windows", top_k=2)
    assert r.status == "ok"
    assert len(r.data["results"]) >= 1
