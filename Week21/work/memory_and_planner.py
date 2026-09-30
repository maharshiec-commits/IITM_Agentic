"""
================================================================================
APEX GLOBAL BANK — MEMORY & MULTI-STEP PLANNER (memory_and_planner.py)
================================================================================
Phase 6: Planning, Memory & Context
Manages multi-turn conversation state, sliding window buffer memory, and
step-by-step reasoning decomposition.
================================================================================
"""

from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate

# Question Condenser Prompt for Resolving Multi-Turn Ambiguity & Pronouns
CONDENSE_PROMPT_TEMPLATE = """You are a conversational query condenser for Apex Bank.
Given the previous chat history and a follow-up inquiry, rewrite the inquiry as an unambiguous standalone question that captures the entire context.

Chat History:
{chat_history}

Follow-up User Inquiry: {question}

Standalone Question:"""

condense_prompt = PromptTemplate.from_template(CONDENSE_PROMPT_TEMPLATE)


class ConversationSession:
    """Encapsulates memory and multi-step planning state for a user session."""

    def __init__(self, session_id: str = "default_user", window_size: int = 6):
        self.session_id = session_id
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output",
            k=window_size
        )
        self.plan_history = []

    def get_chat_history_str(self) -> str:
        """Returns the serialized textual chat history for LLM prompting."""
        messages = self.memory.chat_memory.messages
        if not messages:
            return "No previous conversation."
        
        history_lines = []
        for msg in messages:
            sender = "User" if msg.type == "human" else "Apex Assistant"
            history_lines.append(f"{sender}: {msg.content}")
        return "\n".join(history_lines)

    def add_interaction(self, user_msg: str, agent_response: str):
        """Saves interaction turn to sliding memory."""
        self.memory.save_context({"input": user_msg}, {"output": agent_response})

    def reset_memory(self):
        """Clears conversational history upon user request or session logout."""
        self.memory.clear()
        self.plan_history = []


def decompose_plan(user_query: str) -> list[str]:
    """
    Decomposes an incoming banking inquiry into structured cognitive steps:
    1. Safety check
    2. Tool or Knowledge retrieval identification
    3. Calculation or Policy verification
    4. Safe customer response drafting
    """
    q_lower = user_query.lower()
    plan = ["Step 1: Perform Safety Verification (Ensure non-transactional compliance)"]
    
    # Check if calculation is needed
    if any(w in q_lower for w in ["emi", "calculate", "loan amount", "monthly payment"]):
        plan.append("Step 2: Parse financial parameters and invoke calculate_loan_emi tool")
    
    # Check if account summary is requested
    elif any(w in q_lower for w in ["balance", "cust101", "cust102", "my account", "kyc status"]):
        plan.append("Step 2: Identify Customer ID and invoke check_account_summary tool")
        
    # Check if foreign exchange is requested
    elif any(w in q_lower for w in ["forex", "usd", "eur", "gbp", "exchange rate", "dollar"]):
        plan.append("Step 2: Identify currency pair and invoke get_forex_rates tool")
        
    # Check if escalation / fraud is reported
    elif any(w in q_lower for w in ["fraud", "unauthorized", "stolen", "scam", "dispute", "complaint"]):
        plan.append("Step 2: Identify grievance severity and trigger create_support_escalation_ticket tool")
        
    # Otherwise standard policy RAG
    else:
        plan.append("Step 2: Perform semantic search over banking policy knowledge base")
        
    plan.append("Step 3: Synthesize factual, grounded advisory response without hallucinations")
    plan.append("Step 4: Execute PII-sanitized telemetry logging")
    return plan

