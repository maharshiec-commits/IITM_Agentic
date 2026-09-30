from __future__ import annotations
from typing import Any, Dict, List

def select_relevant_user_memory(user_mem: Dict[str, Any], category: str) -> Dict[str, Any]:
    common = ["os", "device", "preferred_language"]
    vpn = ["vpn_client"]
    access = ["manager_name"]
    security = ["mfa_enabled"]
    allow: List[str] = common.copy()
    if category == "vpn":
        allow += vpn
    if category in ("access", "software_install"):
        allow += access
    if category == "security":
        allow += security
    return {k: user_mem[k] for k in allow if k in user_mem}

def select_relevant_case_memory(case_mem: Dict[str, Any]) -> Dict[str, Any]:
    allow = ["summary", "last_decision"]
    return {k: case_mem[k] for k in allow if k in case_mem}
