from src.tools import registry
from src.agent.agent import run_once

def test_agent_survives_missing_kb_search():
    orig = registry.REGISTRY.get("kb_search")
    registry.REGISTRY.pop("kb_search", None)
    try:
        _, resp = run_once("VPN not connecting. Authentication failed.", user_id="u_test", user_context={"os":"Windows"})
        assert "## 1) Decision:" in resp
    finally:
        if orig:
            registry.REGISTRY["kb_search"] = orig
