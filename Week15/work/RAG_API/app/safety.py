import re
from dataclasses import dataclass
from typing import Tuple, Dict, Any, Optional


INJECTION_PATTERNS = [
    r"ignore (all|previous|earlier) instructions",
    r"disregard (all|previous|earlier) instructions",
    r"reveal (the )?(system|developer) prompt",
    r"show (me )?(your )?(system|hidden) instructions",
    r"act as (an )?(admin|root|developer)",
    r"you are not bound by",
    r"bypass (policy|rules|safety)",
    r"print (the )?entire (document|context)",
    r"dump (all|the) (documents|policies|data)",
]
INJECTION_RE = re.compile("|".join(f"(?:{p})" for p in INJECTION_PATTERNS), re.IGNORECASE)

SENSITIVE_HR_PATTERNS = [
    r"\bsalary\b",
    r"\bcompensation\b",
    r"\bctc\b",
    r"\bpayroll\b",
    r"\bbonus\b",
    r"\bappraisal\b",
    r"\bperformance rating\b",
    r"\bterminate\b",
    r"\bfiring\b",
    r"\blayoff\b",
    r"\bdisciplinary\b",
    r"\bmedical\b",
    r"\bhealth\b",
]
SENSITIVE_HR_RE = re.compile("|".join(f"(?:{p})" for p in SENSITIVE_HR_PATTERNS), re.IGNORECASE)


@dataclass
class SafetyDecision:
    allowed: bool
    reason: Optional[str]
    meta: Dict[str, Any]


def safety_wrapper(user_query: str, *, allow_sensitive: bool = False, max_len: int = 2000) -> SafetyDecision:
    """
    Returns a decision to use downstream (retrieval/logging/LLM).
    """
    meta: Dict[str, Any] = {}

    # Basic input constraints
    if not user_query or not user_query.strip():
        return SafetyDecision(False, "Empty query.", "", meta)
    if len(user_query) > max_len:
        return SafetyDecision(False, f"Query too long (>{max_len} chars).", "", meta)

    # Prompt injection detection
    if INJECTION_RE.search(user_query):
        return SafetyDecision(
            allowed=False,
            reason="Potential prompt-injection / data-exfiltration attempt detected.",
            meta={**meta, "blocked_by": "prompt_injection"},
        )

    # Sensitive HR content gating
    if (not allow_sensitive) and SENSITIVE_HR_RE.search(user_query):
        return SafetyDecision(
            allowed=False,
            reason="This request may involve sensitive HR data. Please use an authorized channel.",
            meta={**meta, "blocked_by": "sensitive_hr"},
        )

    return SafetyDecision(True, None, meta)
