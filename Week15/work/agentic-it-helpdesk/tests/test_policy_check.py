from src.tools.policy_check import policy_check

def test_policy_admin_access_requires_approval():
    r = policy_check("grant_admin_access")
    assert r.status == "ok"
    assert r.data["decision"] == "requires_approval"

def test_policy_unknown_action_defaults_to_requires_approval():
    r = policy_check("some_unknown_action")
    assert r.status == "ok"
    assert r.data["decision"] == "requires_approval"
