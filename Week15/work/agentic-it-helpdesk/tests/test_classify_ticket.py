from src.tools.classify_ticket import classify_ticket

def test_classify_vpn():
    r = classify_ticket("VPN not connecting. Authentication failed.")
    assert r.status == "ok"
    assert r.data["category"] == "vpn"
    assert r.confidence >= 0.7

def test_classify_security():
    r = classify_ticket("Clicked a link and entered OTP, might be phishing.")
    assert r.status == "ok"
    assert r.data["category"] == "security"
    assert r.data["urgency"] == "P1"
    assert r.confidence >= 0.8
