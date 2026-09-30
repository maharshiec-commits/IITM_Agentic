from src.agent.agent import run_once

def test_agent_vpn_runs():
    _, resp = run_once("VPN not connecting. Authentication failed.", user_id="u_test", user_context={"os":"Windows"})
    assert "## 1) Decision:" in resp

def test_agent_security_escalates():
    _, resp = run_once("Clicked a link and entered OTP, phishing suspected.", user_id="u_test", user_context={"device":"Mobile"})
    assert "escalate_to_SecOps" in resp

def test_agent_admin_requires_approval():
    _, resp = run_once("Need admin access to install Docker.", user_id="u_test", user_context={"os":"macOS"})
    assert "requires_approval" in resp
