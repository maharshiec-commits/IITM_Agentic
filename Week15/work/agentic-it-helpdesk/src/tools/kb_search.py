from __future__ import annotations
from typing import Dict, List
from rapidfuzz import fuzz
from src.models import ToolResult
from src.utils import read_json, data_path, safe_lower

def kb_search(query: str, top_k: int = 3) -> ToolResult:
    kb_index: List[Dict] = read_json(data_path("kb_index.json"))
    q = safe_lower(query)
    scored = []
    for item in kb_index:
        text = " ".join([item.get("title", ""), " ".join(item.get("tags", [])), item.get("category", "")])
        score = fuzz.partial_ratio(q, safe_lower(text))
        scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for score, item in scored[:top_k]:
        conf = min(1.0, max(0.3, score / 100.0))
        results.append({
            "kb_id": item["kb_id"],
            "title": item["title"],
            "risk_level": item.get("risk_level", "low"),
            "steps": item.get("steps", []),
            "confidence": conf
        })

    return ToolResult(
        tool="kb_search",
        status="ok",
        data={"results": results},
        confidence=results[0]["confidence"] if results else 0.4,
        audit=[f"kb_search: query='{query}', top_k={top_k}, returned={len(results)}"],
    )
