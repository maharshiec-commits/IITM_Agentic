from __future__ import annotations
import json, os
from datetime import datetime
from typing import Any, Dict, Optional
from dataclasses import asdict
from src.models import TicketCase
from src.agent.metrics import RunMetrics, metrics_to_dict
from src.agent.config import LoggingConfig

class JsonlLogger:
    def __init__(self, cfg: Optional[LoggingConfig] = None) -> None:
        cfg = cfg or LoggingConfig()
        self.log_dir = cfg.dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.audit_path = os.path.join(self.log_dir, cfg.audit_file)
        self.metrics_path = os.path.join(self.log_dir, cfg.metrics_file)

    def log_case(self, run_id: str, case: TicketCase, response: str) -> None:
        record: Dict[str, Any] = {
            "ts": datetime.utcnow().isoformat(),
            "run_id": run_id,
            "case": asdict(case),
            "response": response
        }
        with open(self.audit_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def log_metrics(self, metrics: RunMetrics) -> None:
        record: Dict[str, Any] = {
            "ts": datetime.utcnow().isoformat(),
            **metrics_to_dict(metrics)
        }
        with open(self.metrics_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
