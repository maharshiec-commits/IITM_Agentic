from __future__ import annotations
from typing import Dict, List
from src.models import ToolResult

def generate_resolution_plan(ticket_case: Dict, kb_results: List[Dict]) -> ToolResult:
    if kb_results:
        best = kb_results[0]
        steps = best.get("steps", []).copy()
        checkpoints = ["After each step, confirm whether the issue is resolved (yes/no)."]
        stop_conditions = [
            "If any step requires admin/privileged action, stop and request approval.",
            "If issue persists after steps, prepare escalation note."
        ]
        conf = min(1.0, 0.6 + 0.1 * len(steps))
        return ToolResult(
            tool="generate_resolution_plan",
            status="ok",
            data={"steps": steps, "checkpoints": checkpoints, "stop_conditions": stop_conditions},
            confidence=conf,
            audit=[f"generate_resolution_plan: used KB={best.get('kb_id')} steps={len(steps)}"]
        )
    steps = [
        "Collect OS/device details and exact error message.",
        "Confirm when the issue started and whether it affects others.",
        "Try standard restart/reconnect steps relevant to the issue.",
        "If unresolved, escalate with collected evidence."
    ]
    return ToolResult(
        tool="generate_resolution_plan",
        status="ok",
        data={"steps": steps, "checkpoints": ["Confirm outcome after basic troubleshooting."],
              "stop_conditions": ["If ticket appears security-related, escalate to SecOps immediately."]},
        confidence=0.6,
        audit=["generate_resolution_plan: fallback plan"]
    )
