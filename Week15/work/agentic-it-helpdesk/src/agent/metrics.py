from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, List
import time

@dataclass
class ToolMetric:
    tool: str
    status: str
    latency_ms: float
    confidence: float

@dataclass
class RunMetrics:
    run_id: str
    total_latency_ms: float
    decision: str
    tool_metrics: List[ToolMetric]

class Timer:
    def __init__(self):
        self.t0 = time.perf_counter()
    def stop_ms(self) -> float:
        return (time.perf_counter() - self.t0) * 1000.0

def metrics_to_dict(m: RunMetrics) -> Dict[str, Any]:
    return asdict(m)
