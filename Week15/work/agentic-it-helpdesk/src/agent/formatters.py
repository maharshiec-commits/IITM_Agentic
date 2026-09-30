from __future__ import annotations
from typing import Any, Dict, List, Optional
from src.models import TicketCase

def _bullet(lines: List[str]) -> str:
    return "\n".join([f"- {x}" for x in lines]) if lines else "- (none)"

def format_response(
    case: TicketCase,
    decision: str,
    kb_used: List[Dict[str, Any]],
    plan: Optional[Dict[str, Any]],
    policy_flags: Dict[str, Any],
    escalation: Optional[Dict[str, Any]],
) -> str:
    category = case.classification.get("category", "other")
    subcategory = case.classification.get("subcategory", "unknown")
    urgency = case.classification.get("urgency", "P4")
    reasons = case.classification.get("reasons", [])

    kb_line = []
    for r in kb_used:
        kb_line.append(f"{r.get('kb_id')} — {r.get('title')} (risk={r.get('risk_level')}, conf={r.get('confidence')})")

    steps = (plan or {}).get("steps", [])
    checkpoints = (plan or {}).get("checkpoints", [])
    stop_conditions = (plan or {}).get("stop_conditions", [])

    policy_notes = []
    for d in case.policy.get("decisions", []):
        action = d.get("action")
        pdec = d.get("decision")
        approver = d.get("approver_role", "")
        policy_notes.append(f"{action}: {pdec}" + (f" (approver={approver})" if approver else ""))

    hitl_required = bool(policy_flags.get("hitl_required", False))

    out = []
    out.append(f"## 1) Decision: {decision}")
    out.append("")
    out.append("## 2) Key Findings")
    out.append(_bullet([
        f"classification: category={category}, subcategory={subcategory}",
        f"urgency: {urgency}",
        f"reasoning signals: {', '.join(reasons) if reasons else 'n/a'}"
    ]))
    out.append("")
    out.append("## 3) Steps / Plan")
    if steps:
        out.append("\n".join([f"{i+1}. {s}" for i, s in enumerate(steps)]))
    else:
        out.append("- (no steps yet)")
    if checkpoints:
        out.append("\n**Checkpoints**\n" + _bullet(checkpoints))
    if stop_conditions:
        out.append("\n**Stop Conditions**\n" + _bullet(stop_conditions))
    out.append("")
    out.append("## 4) Policy / Safety")
    safety = [
        "I will NOT perform privileged actions (password reset/access grants) directly.",
        "I will NOT bypass security processes or hide incidents."
    ]
    if policy_notes:
        safety.append("Policy decisions: " + "; ".join(policy_notes))
    if hitl_required:
        safety.append("HITL required: approval/confirmation needed before next step.")
    out.append(_bullet(safety))
    out.append("")
    out.append("## 5) Evidence Used")
    out.append(_bullet([
        "user ticket text",
        f"user context keys: {', '.join(sorted(case.user_context.keys())) if case.user_context else '(none)'}",
        "KB used: " + ("; ".join(kb_line) if kb_line else "(none)")
    ]))
    out.append("")
    out.append("## 6) Next Steps")
    next_steps = []
    if decision == "request_more_info":
        qs = case.missing_info.get("questions", [])
        next_steps.append("Please answer:")
        next_steps.extend([f"Q{i+1}: {q}" for i, q in enumerate(qs)])
    elif decision == "requires_approval":
        next_steps.append("This request requires approval as per policy.")
        next_steps.append("Do you want me to draft an approval request for the approver? (yes/no)")
    elif decision == "escalate_to_SecOps":
        next_steps.append("This is security-sensitive. I will prepare an escalation note to SecOps.")
        next_steps.append("Do you want me to draft and submit the incident report note to SecOps? (yes/no)")
        if escalation:
            next_steps.append("Escalation summary preview:\n" + escalation.get("summary", ""))
    else:
        next_steps.append("Try the steps above and tell me which step fails (if any).")
        next_steps.append("If still unresolved, I will prepare an escalation packet for L2.")
    out.append("\n".join(next_steps))
    return "\n".join(out)
