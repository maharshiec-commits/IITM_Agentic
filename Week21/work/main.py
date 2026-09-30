"""
================================================================================
APEX GLOBAL BANK — CLI INTERACTIVE CONSOLE (main.py)
================================================================================
Interactive terminal runner for ApexBank AI Advisory Copilot.
Type 'exit' to quit, 'clear' to reset conversation memory.
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

PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

from agent import ApexBankingAgent


def run_interactive_cli():
    print("=" * 80)
    print("  APEX GLOBAL BANK — AI ADVISORY COPILOT (CLI)")
    print("  Enterprise Non-Transactional Banking Advisory & Decision Support")
    print("  Type 'exit' to quit | Type 'clear' to reset conversation memory")
    print("=" * 80)

    agent = ApexBankingAgent(session_id="cli_user_session")
    print("\nCopilot: Welcome to Apex Global Bank! How can I assist you today?\n")

    while True:
        try:
            user_input = input("Customer: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nThank you for choosing Apex Global Bank. Goodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Thank you for banking with Apex Global Bank. Goodbye!")
            break
        if user_input.lower() == "clear":
            agent.session.reset_memory()
            print("[Conversational memory cleared.]\n")
            continue

        result = agent.process_query(user_input)
        print(f"\nCopilot: {result['response']}\n")
        if result["tools_used"]:
            print(f"  [Tools Invoked: {', '.join(result['tools_used'])} | Latency: {result['latency_sec']}s | Risk: {result['risk_flag']}]")
        print("-" * 80)


if __name__ == "__main__":
    run_interactive_cli()

