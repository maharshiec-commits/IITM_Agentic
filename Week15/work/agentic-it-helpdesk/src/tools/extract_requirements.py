from __future__ import annotations
from typing import Dict, List
from src.models import ToolResult

CATEGORY_FIELDS = {
    "vpn": ["os", "error_code", "time_started", "network_type", "vpn_client"],
    "password": ["username", "mfa_enabled", "last_successful_login"],
    "access": ["requested_access", "business_justification", "duration_needed", "manager_name"],
    "software_install": ["software_name", "os", "device", "admin_rights_needed"],
    "network": ["os", "network_type", "location", "time_started"],
    "security": ["what_clicked", "otp_entered", "time_started", "device", "email_sender"]
}

def extract_requirements(category: str, ticket_text: str, known_context: Dict = None) -> ToolResult:
    known_context = known_context or {}
    fields = CATEGORY_FIELDS.get(category, ["os", "device", "time_started"])

    fields_needed: List[str] = []
    questions: List[str] = []
    for f in fields:
        if f not in known_context or known_context.get(f) in (None, "", "unknown"):
            fields_needed.append(f)

    for f in fields_needed:
        if f == "os":
            questions.append("Which operating system are you on (Windows/macOS/Linux/Android/iOS)?")
        elif f == "error_code":
            questions.append("What exact error message or error code do you see?")
        elif f == "time_started":
            questions.append("When did the issue start (approx time)?")
        elif f == "network_type":
            questions.append("Are you on office Wi-Fi, home Wi-Fi, or mobile hotspot?")
        elif f == "vpn_client":
            questions.append("Which VPN client/app are you using (name/version if possible)?")
        elif f == "requested_access":
            questions.append("What access exactly do you need (role/group/tool/admin rights)?")
        elif f == "business_justification":
            questions.append("What is the business justification for this access/install request?")
        elif f == "duration_needed":
            questions.append("Is this access needed temporarily or permanently? If temporary, for how long?")
        elif f == "manager_name":
            questions.append("Who is your approving manager (name/email)?")
        elif f == "software_name":
            questions.append("Which software do you want to install (exact name/version)?")
        elif f == "admin_rights_needed":
            questions.append("Does the installation require admin privileges (yes/no/unsure)?")
        elif f == "what_clicked":
            questions.append("What did you click (link/attachment)? If possible, paste the URL/domain (do not open it again).")
        elif f == "otp_entered":
            questions.append("Did you enter OTP or credentials on that page (yes/no)?")
        elif f == "email_sender":
            questions.append("What was the email sender address/domain?")
        else:
            questions.append(f"Please provide: {f}")

    return ToolResult(
        tool="extract_requirements",
        status="ok",
        data={"fields_needed": fields_needed, "questions": questions},
        confidence=0.85 if len(fields_needed) <= 3 else 0.75,
        audit=[f"extract_requirements: category={category}, missing={len(fields_needed)}"],
    )
