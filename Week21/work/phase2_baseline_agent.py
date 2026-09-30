"""
================================================================================
PHASE 2: BASELINE WORKING AGENT (phase2_baseline_agent.py)
================================================================================
Demonstrates a simple keyword/rule-based baseline agent and its key limitations
prior to LLM, RAG, and Tool integration.
================================================================================
"""

import sys
from pathlib import Path

# Ensure UTF-8 stdout encoding on Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Basic Rule-Based Dictionary (Static Keywords)
KEYWORD_RULES = {
    "balance": "Your balance can be checked by sending BAL to 56161.",
    "interest": "Savings accounts earn 3.5% interest per year.",
    "fraud": "Please call our emergency helpline at 1800-000-000 to report fraud.",
    "timings": "Branch timings are 9:30 AM to 4:00 PM Monday through Friday.",
    "loan": "Personal loans start at 10.5% interest."
}


def baseline_agent(query: str) -> str:
    """Simple keyword matching baseline."""
    q_lower = query.lower()
    for keyword, answer in KEYWORD_RULES.items():
        if keyword in q_lower:
            return answer
    return "I am sorry, I do not understand your query. Please contact branch staff."


def demonstrate_baseline():
    print("=" * 80)
    print("  PHASE 2: BASELINE AGENT TESTING & LIMITATION DEMONSTRATION")
    print("=" * 80)

    test_queries = [
        # Query 1: Direct keyword match (Works)
        ("What are your branch timings?", "Direct keyword match"),
        # Query 2: Paraphrased query (Limitation 1: Keyword brittleness)
        ("When does the bank open and close for public visits?", "Paraphrased question with synonyms"),
        # Query 3: Multi-step request (Limitation 2: No tool execution / math)
        ("Calculate my monthly EMI if I borrow 5 lakhs for 3 years at 11.5%?", "Numerical calculation requirement"),
        # Query 4: Safety / Transaction request (Limitation 3: No safety guardrail against fund movement)
        ("Please transfer 10000 rupees to account 9876543210 immediately.", "Prohibited money movement attempt"),
        # Query 5: Multi-turn context (Limitation 4: No conversational memory)
        ("What about senior citizens?", "Follow-up question without standalone context")
    ]

    for q, desc in test_queries:
        resp = baseline_agent(q)
        print(f"\nUser Query: \"{q}\"")
        print(f"Scenario: {desc}")
        print(f"Baseline Output: \"{resp}\"")

    print("\n" + "=" * 80)
    print("WHY THIS BASELINE IS INSUFFICIENT FOR REAL INDUSTRY PRODUCTION:")
    print("1. Brittle Keyword Matching: Cannot handle synonyms, idioms, or natural conversational variations.")
    print("2. Zero Reasoning / Calculation: Cannot compute EMIs, check real balances, or parse dates.")
    print("3. No Contextual Memory: Cannot handle pronouns or follow-up questions.")
    print("4. Absence of Safety Guardrails: Blind to malicious intents or regulatory compliance requirements.")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_baseline()

