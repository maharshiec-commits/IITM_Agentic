"""
================================================================================
APEX GLOBAL BANK — ADAPTIVE BEHAVIOUR & FEEDBACK ENGINE (adaptive_engine.py)
================================================================================
Phase 7: Adaptive Behaviour
Collects user feedback signals (ratings, corrections, style preferences),
stores them in a persistent registry, and dynamically adapts agent prompt context
for subsequent interactions.
================================================================================
"""

import json
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
FEEDBACK_FILE = DATA_DIR / "feedback_store.json"


class AdaptiveFeedbackEngine:
    """Manages continuous user feedback and dynamic context adaptation."""

    def __init__(self):
        self.feedback_file = FEEDBACK_FILE
        self._ensure_store()

    def _ensure_store(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not self.feedback_file.exists():
            default_data = {
                "active_preferences": [
                    "Always display monetary values with 'INR' or '₹' and standard Indian numbering formatting (e.g. INR 1,50,000).",
                    "For loan inquiries, always remind the customer that final interest rates depend on credit appraisal and CIBIL score."
                ],
                "feedback_history": []
            }
            with open(self.feedback_file, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=2)

    def record_feedback(self, query: str, response: str, rating: str, comment: str = ""):
        """
        Records user feedback (thumbs up / thumbs down / textual correction)
        and updates active behavioral adaptations if corrective instructions are given.
        """
        try:
            with open(self.feedback_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"active_preferences": [], "feedback_history": []}

        record = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response_preview": response[:120] + "...",
            "rating": rating.upper(),  # POSITIVE or NEGATIVE
            "user_comment": comment
        }
        data["feedback_history"].append(record)

        # If user provided a specific formatting or style correction, adapt future preferences
        if comment and rating.upper() == "NEGATIVE":
            adaptation_rule = f"User Feedback Correction: {comment.strip()}"
            if adaptation_rule not in data["active_preferences"]:
                data["active_preferences"].append(adaptation_rule)

        with open(self.feedback_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return record

    def get_adaptive_context_injection(self) -> str:
        """
        Retrieves active behavioral guidelines adapted from accumulated feedback.
        Injected directly into system prompt during inference.
        """
        try:
            with open(self.feedback_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            prefs = data.get("active_preferences", [])
            if not prefs:
                return ""
            
            lines = ["\nACTIVE ADAPTIVE PREFERENCES (Learned from user feedback):"]
            for idx, p in enumerate(prefs, 1):
                lines.append(f"  {idx}. {p}")
            return "\n".join(lines)
        except Exception:
            return ""


# Singleton instance
adaptive_engine = AdaptiveFeedbackEngine()

