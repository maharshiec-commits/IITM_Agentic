from __future__ import annotations
import json, os
from typing import Any

def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def safe_lower(s: str) -> str:
    return (s or "").lower().strip()

def data_path(*parts: str) -> str:
    base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    return os.path.join(base, *parts)
