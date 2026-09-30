from __future__ import annotations
from typing import Dict
from src.models import ToolResult
from src.utils import read_json, data_path

def policy_check(action: str, context: Dict = None) -> ToolResult:
    rules = read_json(data_path("policy_rules.json"))
    rule = rules.get(action)
    if not rule:
        return ToolResult(
            tool="policy_check",
            status="ok",
            data={"decision": "requires_approval", "approver_role": "L1_Lead",
                  "reasons": [f"No explicit rule for action '{action}'. Defaulting to requires_approval."]},
            confidence=0.7,
            audit=[f"policy_check: action={action} default requires_approval"]
        )
    return ToolResult(
        tool="policy_check",
        status="ok",
        data={"decision": rule["decision"], "approver_role": rule.get("approver_role", ""), "reasons": rule.get("reasons", [])},
        confidence=0.9,
        audit=[f"policy_check: action={action} decision={rule['decision']}"]
    )
