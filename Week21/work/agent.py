"""
================================================================================
APEX GLOBAL BANK — AI ADVISORY & SUPPORT COPILOT (agent.py)
================================================================================
Industry Capstone Project: Autonomous Agent for Non-Transactional Banking
Coordinates Safety Guardrails, Task Planning, Vector RAG Retrieval, Deterministic
Tool Invocation, Conversational Memory, and PII-Safe Telemetry.
================================================================================
"""

import os
import sys
import time
import json
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 stdout encoding on Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from tools import (
    check_action_safety,
    check_account_summary,
    calculate_loan_emi,
    get_forex_rates,
    create_support_escalation_ticket,
    MOCK_CUSTOMERS
)
from rag_engine import retrieve_context
from memory_and_planner import ConversationSession, decompose_plan
from adaptive_engine import adaptive_engine
from safe_logger import safe_logger, sanitize_pii

PROJECT_DIR = Path(__file__).parent


def get_llm():
    """Initializes ChatOpenAI instance using .env credentials."""
    load_dotenv(PROJECT_DIR / ".env")
    api_key = os.environ.get("OPENAI_API_KEY")
    api_base = os.environ.get("OPENAI_API_BASE")
    model = os.environ.get("MODEL", "gpt-4o-mini")

    kwargs = {"model": model, "temperature": 0.1, "openai_api_key": api_key}
    if api_base:
        kwargs["openai_api_base"] = api_base
    return ChatOpenAI(**kwargs)


class ApexBankingAgent:
    """Production AI Banking Support & Advisory Agent (Non-Transactional)."""

    def __init__(self, session_id: str = "user_default"):
        self.session = ConversationSession(session_id=session_id)
        self.llm = get_llm()

    def process_query(self, user_query: str) -> dict:
        """
        Processes an incoming customer query through the 6-stage cognitive agent pipeline:
        1. Safety verification
        2. Plan decomposition
        3. Tool or RAG execution
        4. LLM synthesis with adaptive prompt
        5. Memory persistence
        6. PII-safe logging & latency tracking
        """
        start_time = time.time()
        tools_called = []
        risk_level = "LOW"
        sources = []

        # ── STAGE 1: SAFETY GUARDRAIL VERIFICATION ───────────────────────────
        is_safe, refusal_msg = check_action_safety(user_query)
        if not is_safe:
            latency = time.time() - start_time
            safe_logger.log_safety_violation(self.session.session_id, user_query, refusal_msg)
            safe_logger.log_interaction(
                self.session.session_id, user_query, refusal_msg, latency, ["SAFETY_GUARDRAIL_BLOCKED"], "HIGH"
            )
            self.session.add_interaction(user_query, refusal_msg)
            return {
                "response": refusal_msg,
                "plan": ["Step 1: Prohibited action intercepted by Safety Guardrail"],
                "tools_used": ["SAFETY_GUARDRAIL_BLOCKED"],
                "sources": [],
                "risk_flag": "HIGH",
                "latency_sec": round(latency, 3)
            }

        # ── STAGE 2: MULTI-STEP PLAN DECOMPOSITION ───────────────────────────
        plan = decompose_plan(user_query)
        q_lower = user_query.lower()

        # ── STAGE 3: TOOL EXECUTION & CONTEXT RETRIEVAL ───────────────────────
        tool_results = []

        # Tool 1: Account summary check
        for cid in MOCK_CUSTOMERS.keys():
            if cid.lower() in q_lower or (cid == "CUST101" and "my account" in q_lower):
                tool_out = check_account_summary(cid)
                tool_results.append(f"[Tool: check_account_summary for {cid}]\n{tool_out}")
                tools_called.append("check_account_summary")
                break

        # Tool 2: Loan EMI computation
        if any(w in q_lower for w in ["emi", "calculate emi", "monthly emi"]):
            # Extract basic numerical arguments or use defaults
            import re
            numbers = [float(n.replace(",", "")) for n in re.findall(r'\b\d+(?:,\d+)*(?:\.\d+)?\b', user_query)]
            # If principal, rate, tenure are specified in query
            if len(numbers) >= 3:
                p, r, t = numbers[0], numbers[1], int(numbers[2])
                tool_out = calculate_loan_emi(p, r, t)
                tool_results.append(f"[Tool: calculate_loan_emi]\n{tool_out}")
                tools_called.append("calculate_loan_emi")
            elif "personal loan" in q_lower:
                # Demonstration calculation (e.g. 5,00,000 @ 11.5% for 36 months)
                tool_out = calculate_loan_emi(500000, 11.5, 36)
                tool_results.append(f"[Tool: calculate_loan_emi for sample INR 5,00,000 @ 11.5% 36m]\n{tool_out}")
                tools_called.append("calculate_loan_emi")

        # Tool 3: Forex rate lookup
        for pair in ["USD/INR", "EUR/INR", "GBP/INR", "AED/INR", "SGD/INR"]:
            curr = pair.split("/")[0].lower()
            if curr in q_lower or pair.lower() in q_lower:
                tool_out = get_forex_rates(pair)
                tool_results.append(f"[Tool: get_forex_rates for {pair}]\n{tool_out}")
                tools_called.append("get_forex_rates")
                break

        # Tool 4: Support Escalation Ticket creation
        if any(w in q_lower for w in ["fraud", "unauthorized", "stolen card", "compromised", "scam"]):
            risk_level = "CRITICAL"
            cid = "CUST101" if "cust101" in q_lower else ("CUST102" if "cust102" in q_lower else "GUEST")
            ticket_out = create_support_escalation_ticket(cid, "Fraud & Security", "CRITICAL", user_query[:100])
            tool_results.append(f"[Tool: create_support_escalation_ticket]\n{ticket_out}")
            tools_called.append("create_support_escalation_ticket")

        # Knowledge Base RAG Retrieval
        rag_context, sources = retrieve_context(user_query, top_k=3)

        # ── STAGE 4: PROMPT SYNTHESIS WITH ADAPTIVE PREFERENCES ──────────────
        adaptive_rules = adaptive_engine.get_adaptive_context_injection()
        chat_history = self.session.get_chat_history_str()

        system_prompt = f"""You are ApexBank AI Copilot, a senior advisory AI consultant for Apex Global Bank.
Your role is to assist retail and business customers with accurate, polite, and grounded banking information.

STRICT MANDATES & POLICIES:
1. NON-TRANSACTIONAL ADVISORY ONLY: Never execute fund transfers, money movements, password changes, or account approvals. Refuse politely if asked.
2. ZERO HALLUCINATION: Quote exact interest rates, fees, and rules strictly from the provided Knowledge Base context.
3. EXPLAIN UNCERTAINTY: If an answer is not covered in the knowledge base or tool outputs, clearly state your uncertainty instead of guessing.
4. ESCALATE HIGH-RISK: If fraud or unauthorized access is reported, confirm ticket creation and give the 24x7 emergency hotline: 1800-APEX-SECURE (1800-273-9732).
5. PII AWARENESS: Never reveal unmasked account numbers, card CVVs, or full Aadhaar numbers.

{adaptive_rules}

CONVERSATION HISTORY:
{chat_history}

RETRIEVED KNOWLEDGE BASE CONTEXT:
{rag_context}

TOOL EXECUTION RESULTS:
{chr(10).join(tool_results) if tool_results else "No external tools required."}
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_query)
        ]

        llm_response = self.llm.invoke(messages)
        final_answer = llm_response.content.strip()

        # ── STAGE 5: MEMORY UPDATE & STAGE 6: PII-SAFE TELEMETRY ─────────────
        self.session.add_interaction(user_query, final_answer)
        latency = time.time() - start_time
        safe_logger.log_interaction(
            self.session.session_id, user_query, final_answer, latency, tools_called, risk_level
        )

        return {
            "response": final_answer,
            "plan": plan,
            "tools_used": tools_called,
            "sources": sources,
            "risk_flag": risk_level,
            "latency_sec": round(latency, 3)
        }

