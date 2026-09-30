"""
================================================================================
APEX GLOBAL BANK — SAFE LOGGER & PII SANITIZATION ENGINE (safe_logger.py)
================================================================================
Phase 8: Deployment Readiness & Safety Enforcement
This module ensures that NO Personally Identifiable Information (PII) such as
Credit/Debit Card numbers, Bank Account numbers, Aadhaar IDs, Emails, or Phone
numbers are persisted in logs, telemetry, or traces.
================================================================================
"""

import re
import json
import logging
import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
LOGS_DIR = PROJECT_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Regex Patterns for PII Detection
PATTERNS = {
    # 16-digit card numbers (grouped or ungrouped)
    "card_number": re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b'),
    # 9 to 18 digit bank account numbers
    "account_number": re.compile(r'\b(?:Account|Acc|A/c|Acct)?[:\s#]*(\d{9,18})\b', re.IGNORECASE),
    # Indian 12-digit Aadhaar number
    "aadhaar_number": re.compile(r'\b\d{4}\s\d{4}\s\d{4}\b'),
    # Email addresses
    "email_address": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
    # 10-digit Indian phone numbers with optional country code
    "phone_number": re.compile(r'\b(?:\+91[-\s]?)?[6-9]\d{9}\b'),
    # 10-character Indian PAN card format (ABCDE1234F)
    "pan_number": re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'),
}


def sanitize_pii(text: str) -> str:
    """
    Sanitizes and masks any detected PII in the input text string.
    Replaces sensitive tokens with redacted tokens like [REDACTED_CARD_NUMBER].
    """
    if not isinstance(text, str):
        text = str(text)

    sanitized = text
    sanitized = PATTERNS["card_number"].sub("[REDACTED_CARD_NUMBER]", sanitized)
    sanitized = PATTERNS["aadhaar_number"].sub("[REDACTED_AADHAAR]", sanitized)
    sanitized = PATTERNS["pan_number"].sub("[REDACTED_PAN]", sanitized)
    sanitized = PATTERNS["email_address"].sub("[REDACTED_EMAIL]", sanitized)
    sanitized = PATTERNS["phone_number"].sub("[REDACTED_PHONE]", sanitized)
    # Account number sanitization (protecting standalone numerical account identifiers)
    sanitized = PATTERNS["account_number"].sub("Account [REDACTED_ACCOUNT]", sanitized)

    return sanitized


class SafeLogger:
    """Production PII-safe structured logger for audit trails, latency, and telemetry."""

    def __init__(self, log_filename="telemetry_audit.log"):
        self.log_file = LOGS_DIR / log_filename
        self.logger = logging.getLogger("ApexBankSafeLogger")
        self.logger.setLevel(logging.INFO)
        
        # Avoid duplicate handlers
        if not self.logger.handlers:
            fh = logging.FileHandler(str(self.log_file), encoding="utf-8")
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def log_interaction(self, session_id: str, user_input: str, response: str, latency_sec: float, tools_used: list, risk_flag: str = "LOW"):
        """Logs a complete sanitized interaction record."""
        clean_input = sanitize_pii(user_input)
        clean_response = sanitize_pii(response)
        
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "session_id": session_id,
            "user_query_sanitized": clean_input,
            "response_sanitized": clean_response,
            "latency_seconds": round(latency_sec, 3),
            "tools_called": tools_used,
            "risk_assessment": risk_flag
        }
        
        self.logger.info(json.dumps(entry))
        return entry

    def log_safety_violation(self, session_id: str, attempted_action: str, reason: str):
        """Logs safety guardrail trigger events."""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event_type": "SAFETY_GUARD_BLOCKED",
            "session_id": session_id,
            "attempted_action": sanitize_pii(attempted_action),
            "refusal_reason": reason
        }
        self.logger.warning(json.dumps(entry))
        return entry


# Singleton instance for application-wide logging
safe_logger = SafeLogger()

