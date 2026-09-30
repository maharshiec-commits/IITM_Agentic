import re

# Simple regex-based masking (demo-friendly; upgrade later with Presidio/DLP/NER)
_PATTERNS = [
    ("EMAIL", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("PHONE", re.compile(r"(\+?\d{1,3}[\s-]?)?([6-9]\d{9})\b")),                 # IN-like 10-digit
    ("PHONE", re.compile(r"\b\d{3}[-\s]?\d{3}[-\s]?\d{4}\b")),                   # US-like
    ("CARD",  re.compile(r"\b(?:\d[ -]*?){13,19}\b")),                           # card-ish
    ("PAN",   re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b")),                             # India PAN
    ("ID",    re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")),                          # Aadhaar-like 12 digits
]

def mask_private_data(text: str) -> str:
    if not text:
        return text
    masked = text
    for tag, pattern in _PATTERNS:
        masked = pattern.sub(f"[{tag}]", masked)
    return masked