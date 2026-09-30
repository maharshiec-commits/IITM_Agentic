from __future__ import annotations
from typing import Callable, Dict, Tuple
from src.models import ToolResult
from src.agent.metrics import Timer, ToolMetric

from src.tools.classify_ticket import classify_ticket
from src.tools.extract_requirements import extract_requirements
from src.tools.kb_search import kb_search
from src.tools.policy_check import policy_check
from src.tools.generate_resolution_plan import generate_resolution_plan
from src.tools.create_escalation_note import create_escalation_note

ToolFn = Callable[..., ToolResult]

REGISTRY: Dict[str, ToolFn] = {
    "classify_ticket": classify_ticket,
    "extract_requirements": extract_requirements,
    "kb_search": kb_search,
    "policy_check": policy_check,
    "generate_resolution_plan": generate_resolution_plan,
    "create_escalation_note": create_escalation_note,
}

def run_tool(name: str, **kwargs) -> ToolResult:
    if name not in REGISTRY:
        return ToolResult(tool=name, status="error", error=f"Unknown tool: {name}", confidence=0.0)
    return REGISTRY[name](**kwargs)  # type: ignore

def run_tool_timed(name: str, **kwargs) -> Tuple[ToolResult, ToolMetric]:
    timer = Timer()
    try:
        tr = run_tool(name, **kwargs)
    except Exception as e:
        tr = ToolResult(tool=name, status="error", error=str(e), confidence=0.0, data={})
    latency = timer.stop_ms()
    metric = ToolMetric(tool=name, status=tr.status, latency_ms=latency, confidence=float(tr.confidence or 0.0))
    return tr, metric
