from __future__ import annotations
from typing import Dict, List
from src.models import ToolResult

def create_escalation_note(ticket_case: Dict, evidence: Dict, target_team: str) -> ToolResult:
    classification = ticket_case.get("classification", {})
    urgency = classification.get("urgency", "P4")
    category = classification.get("category", "other")
    summary = f"Escalation to {target_team} | urgency={urgency} | category={category}\nTicket: {ticket_case.get('ticket_text','')[:200]}"
    what_tried: List[str] = evidence.get("what_tried", [])
    recommended_next_action = evidence.get("recommended_next_action", "Please investigate with logs and user context.")
    risk_notes: List[str] = evidence.get("risk_notes", [])
    if category == "security" and not any("security incident" in x.lower() for x in risk_notes):
        risk_notes.append("Treat as potential security incident; preserve evidence and follow IR process.")
    return ToolResult(
        tool="create_escalation_note",
        status="ok",
        data={"summary": summary, "what_was_tried": what_tried,
              "recommended_next_action": recommended_next_action, "risk_notes": risk_notes},
        confidence=0.8,
        audit=[f"create_escalation_note: target={target_team}, category={category}, urgency={urgency}"]
    )
