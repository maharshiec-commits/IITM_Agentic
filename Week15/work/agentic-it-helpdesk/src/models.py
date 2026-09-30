from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class ToolResult:
    tool: str
    status: str
    data: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    audit: List[str] = field(default_factory=list)
    error: Optional[str] = None

@dataclass
class TicketCase:
    case_id: str
    ticket_id: Optional[str]
    user_id: str
    ticket_text: str
    user_context: Dict[str, Any] = field(default_factory=dict)

    classification: Dict[str, Any] = field(default_factory=dict)
    missing_info: Dict[str, Any] = field(default_factory=dict)
    kb_results: List[Dict[str, Any]] = field(default_factory=list)
    plan: Dict[str, Any] = field(default_factory=dict)
    policy: Dict[str, Any] = field(default_factory=dict)
    escalation: Dict[str, Any] = field(default_factory=dict)

    audit_log: List[Dict[str, Any]] = field(default_factory=list)
