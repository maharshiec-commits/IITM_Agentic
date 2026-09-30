from src.tools.create_escalation_note import create_escalation_note

def test_escalation_note_security_adds_risk_note():
    ticket_case = {"ticket_text":"clicked link", "classification":{"category":"security","urgency":"P1"}}
    evidence = {"what_tried": [], "recommended_next_action":"IR followup", "risk_notes":[]}
    r = create_escalation_note(ticket_case, evidence, target_team="SecOps")
    assert r.status == "ok"
    assert any("security incident" in x.lower() for x in r.data["risk_notes"])
