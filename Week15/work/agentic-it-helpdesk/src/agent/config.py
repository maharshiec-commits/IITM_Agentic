from __future__ import annotations
import os, yaml
from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass
class AgentConfig:
    conf_threshold: float = 0.70
    kb_top_k: int = 3

@dataclass
class LoggingConfig:
    dir: str = "logs"
    audit_file: str = "runs.jsonl"
    metrics_file: str = "metrics.jsonl"

@dataclass
class PolicyConfig:
    always_escalate_security: bool = True
    require_approval_for: List[str] = None  # type: ignore

@dataclass
class AppConfig:
    agent: AgentConfig
    logging: LoggingConfig
    policy: PolicyConfig

def load_config(path: str = "config/default.yaml") -> AppConfig:
    if not os.path.exists(path):
        return AppConfig(
            agent=AgentConfig(),
            logging=LoggingConfig(),
            policy=PolicyConfig(always_escalate_security=True, require_approval_for=["password_reset","grant_admin_access"]),
        )
    with open(path, "r", encoding="utf-8") as f:
        raw: Dict[str, Any] = yaml.safe_load(f) or {}

    agent = raw.get("agent", {})
    logging = raw.get("logging", {})
    policy = raw.get("policy", {})

    return AppConfig(
        agent=AgentConfig(
            conf_threshold=float(agent.get("conf_threshold", 0.70)),
            kb_top_k=int(agent.get("kb_top_k", 3)),
        ),
        logging=LoggingConfig(
            dir=str(logging.get("dir", "logs")),
            audit_file=str(logging.get("audit_file", "runs.jsonl")),
            metrics_file=str(logging.get("metrics_file", "metrics.jsonl")),
        ),
        policy=PolicyConfig(
            always_escalate_security=bool(policy.get("always_escalate_security", True)),
            require_approval_for=list(policy.get("require_approval_for", ["password_reset","grant_admin_access"])),
        ),
    )
