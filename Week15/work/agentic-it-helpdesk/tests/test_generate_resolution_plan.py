from src.tools.generate_resolution_plan import generate_resolution_plan

def test_generate_plan_uses_kb_steps():
    r = generate_resolution_plan({"classification":{"category":"vpn"}}, [{"kb_id":"KB","steps":["A","B"]}])
    assert r.status == "ok"
    assert r.data["steps"] == ["A","B"]
