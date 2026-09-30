from src.tools.extract_requirements import extract_requirements

def test_extract_requirements_vpn_missing_fields():
    r = extract_requirements("vpn", "VPN auth failed", known_context={"os":"Windows"})
    assert r.status == "ok"
    assert "error_code" in r.data["fields_needed"]
    assert len(r.data["questions"]) >= 1
