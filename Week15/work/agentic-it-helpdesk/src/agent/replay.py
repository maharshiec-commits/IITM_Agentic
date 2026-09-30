from __future__ import annotations
from typing import Dict, Any, List, Optional
from src.agent.agent import run_once
from src.agent.logging import JsonlLogger

def replay_cases(cases: List[Dict[str, Any]], user_id: str, logger: Optional[JsonlLogger] = None) -> List[str]:
    logger = logger or JsonlLogger()
    outputs = []
    for c in cases:
        _, response = run_once(
            ticket_text=c["ticket_text"],
            ticket_id=c.get("ticket_id"),
            user_id=user_id,
            user_context=c.get("user_context", {}),
            logger=logger
        )
        outputs.append(response)
    return outputs
