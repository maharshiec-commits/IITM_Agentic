from __future__ import annotations
from typing import Dict, List, Any

def summarize_for_case_memory(plan_steps: List[str], kb_used_ids: List[str], last_questions: List[str], decision: str) -> Dict[str, Any]:
    return {
        "last_decision": decision,
        "kb_used": kb_used_ids,
        "steps_suggested": plan_steps[:4],
        "last_questions": last_questions[:5],
    }
