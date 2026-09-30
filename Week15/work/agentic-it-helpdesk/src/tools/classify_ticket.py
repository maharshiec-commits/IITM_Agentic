from __future__ import annotations
import re
from typing import List
from src.models import ToolResult
from src.utils import safe_lower

SECURITY_KEYWORDS = ["phishing", "otp", "malware", "ransomware", "suspicious", "clicked link", "credential"]
VPN_KEYWORDS = ["vpn", "authentication failed", "auth failed", "cannot connect vpn"]
PASSWORD_KEYWORDS = ["password", "reset", "forgot password", "locked out"]
ACCESS_KEYWORDS = ["admin access", "permission", "access", "grant", "role", "privilege"]
INSTALL_KEYWORDS = ["install", "setup", "docker", "vscode", "software"]
NETWORK_KEYWORDS = ["wifi", "network", "internet", "dns"]

def _contains_any(text: str, phrases: List[str]) -> bool:
    t = safe_lower(text)
    return any(p in t for p in phrases)

def classify_ticket(ticket_text: str) -> ToolResult:
    t = safe_lower(ticket_text)
    category, subcategory, urgency, confidence = "other", "unknown", "P4", 0.55
    reasons: List[str] = []

    if _contains_any(t, SECURITY_KEYWORDS):
        category, subcategory, urgency, confidence = "security", "suspicious_activity", "P1", 0.9
        reasons.append("Security keywords detected (e.g., phishing/OTP/malware).")
    elif _contains_any(t, VPN_KEYWORDS):
        category, subcategory, urgency, confidence = "vpn", "connectivity_or_auth", "P3", 0.85
        reasons.append("VPN keywords detected + auth/connectivity phrase.")
    elif _contains_any(t, PASSWORD_KEYWORDS):
        category, subcategory, urgency, confidence = "password", "reset_or_lockout", "P2", 0.8
        reasons.append("Password reset/lockout keywords detected.")
    elif _contains_any(t, ACCESS_KEYWORDS):
        category, subcategory, urgency, confidence = "access", "privileged_or_role_access", "P2", 0.78
        reasons.append("Access/permission/admin keywords detected.")
    elif _contains_any(t, INSTALL_KEYWORDS):
        category, subcategory, urgency, confidence = "software_install", "install_request", "P3", 0.75
        reasons.append("Software install keywords detected.")
    elif _contains_any(t, NETWORK_KEYWORDS):
        category, subcategory, urgency, confidence = "network", "wifi_or_dns", "P3", 0.72
        reasons.append("Network/Wi-Fi keywords detected.")

    if re.search(r"\b(entire team|everyone|all users|many users)\b", t):
        urgency = "P1"
        confidence = max(confidence, 0.75)
        reasons.append("Potential widespread impact phrase detected.")

    return ToolResult(
        tool="classify_ticket",
        status="ok",
        data={"category": category, "subcategory": subcategory, "urgency": urgency, "reasons": reasons},
        confidence=confidence,
        audit=[f"classify_ticket: category={category}, urgency={urgency}, conf={confidence:.2f}"],
    )
