"""
================================================================================
APEX GLOBAL BANK — AI ADVISORY COPILOT (app.py)
================================================================================
Industry Capstone Project: Interactive Streamlit UI
Scenario 2: Banking — AI Banking Support & Advisory Agent (Non-Transactional)
Includes Live Visual Langflow Pipeline Inspector, RAG Policy Viewer, and
PII-Sanitized Telemetry Audit Explorer.
================================================================================
"""

import os
import sys
import time
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

from agent import ApexBankingAgent
from adaptive_engine import adaptive_engine
from safe_logger import sanitize_pii

st.set_page_config(
    page_title="ApexBank AI Advisory Copilot",
    page_icon="🏦",
    layout="wide",
)

# Custom Styling
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1e3a8a; margin-bottom: 0px; }
    .sub-title { font-size: 1.05rem; color: #475569; margin-bottom: 1.2rem; }
    .safety-badge { background-color: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
    .tool-badge { background-color: #e0f2fe; color: #0369a1; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_agent():
    return ApexBankingAgent(session_id="streamlit_user_session")


# Sidebar: Customer Persona, Quick Actions & Feedback Store
with st.sidebar:
    st.markdown("### 🏦 Apex Global Bank")
    st.markdown("**AI Advisory & Support Copilot**")
    st.caption("Non-Transactional Advisory & Decision Support")
    st.divider()

    st.subheader("👤 Active User Persona")
    st.markdown("""
    **Customer**: Priya Sharma (`CUST101`)  
    **Segment**: Classic Savings  
    **Branch**: Jubilee Hills, Hyderabad  
    **KYC Status**: Verified (till 2029)  
    """)
    st.divider()

    st.subheader("⚡ Quick Test Scenarios")
    sample_queries = [
        "Can you check the current balance and KYC status for customer CUST101?",
        "Calculate the monthly EMI for a personal loan of 500000 at 11.5% interest for 36 months.",
        "What are the interest rates for Fixed Deposits?",
        "What about senior citizens on the special 444 days tenure?",
        "What are the annual rental charges for a medium locker, and what fixed deposit is required?",
        "Please transfer INR 25,000 to account 9876543210 (Safety Guardrail Test)",
        "I lost my debit card and just saw an unauthorized withdrawal! This is fraud, block it and escalate!"
    ]
    for q in sample_queries:
        if st.button(q, key=f"btn_{q}", use_container_width=True):
            st.session_state.pending_query = q

    st.divider()
    if st.button("🧹 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        agent = get_agent()
        agent.session.reset_memory()
        st.rerun()


# Initialize state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome to Apex Global Bank! I am your AI Advisory Copilot. I can assist you with account inquiries, loan EMI calculations, fixed deposit rates, foreign exchange, and policy guidance. How may I assist your financial journey today?",
            "meta": {}
        }
    ]

agent = get_agent()

# Handle sidebar button clicks
if "pending_query" in st.session_state:
    user_input = st.session_state.pop("pending_query")
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Processing inquiry through cognitive pipeline..."):
        res = agent.process_query(user_input)
    st.session_state.messages.append({
        "role": "assistant",
        "content": res["response"],
        "meta": {
            "plan": res["plan"],
            "tools": res["tools_used"],
            "sources": res["sources"],
            "risk": res["risk_flag"],
            "latency": res["latency_sec"]
        }
    })
    st.rerun()

# Header
st.markdown('<div class="main-title">ApexBank AI Advisory & Support Copilot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Enterprise Non-Transactional Advisory System | Phase 1–9 Capstone Implementation</div>', unsafe_allow_html=True)

# Main Navigation Tabs
tab_chat, tab_visual, tab_policies, tab_audit = st.tabs([
    "💬 Advisory Chatbot",
    "📐 Visual Langflow Pipeline",
    "📚 Banking Policies (RAG)",
    "🔒 PII Audit Telemetry"
])

with tab_chat:
    # Render chat messages inside chat tab
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            meta = msg.get("meta", {})
            if meta and meta.get("tools"):
                with st.expander("🔍 Cognitive Execution Telemetry"):
                    st.markdown(f"**Cognitive Plan**: {' ➔ '.join(meta.get('plan', []))}")
                    st.markdown(f"**Tools Executed**: `{', '.join(meta.get('tools', []))}`")
                    if meta.get("sources"):
                        st.markdown(f"**RAG Citations**: `{', '.join(meta.get('sources', []))}`")
                    st.markdown(f"**Risk Flag**: `{meta.get('risk', 'LOW')}` | **Latency**: `{meta.get('latency', 0.0)}s`")


with tab_visual:
    st.subheader("Interactive Langflow Visual Pipeline Canvas")
    st.caption("Visual representation of apex_bank_copilot_langflow.json. Pan, zoom, drag nodes, and click on any node to view its parameters.")
    
    html_file = PROJECT_DIR / "visual_pipeline.html"
    if html_file.exists():
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=680, scrolling=True)
    else:
        st.info("Visual pipeline file not found. Please check visual_pipeline.html.")


with tab_policies:
    st.subheader("Authoritative Regulatory Policy Corpus (RAG Source)")
    st.markdown("These 4 documents form the grounded semantic knowledge base for the vector search engine:")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("📄 Core Banking & Transaction Policies (AGB-POL-2026-V3)"):
            with open(PROJECT_DIR / "data" / "banking_policies.txt", "r", encoding="utf-8") as f:
                st.text(f.read())
        with col2:
            with st.expander("📄 KYC & Compliance Guidelines (AGB-KYC-2026-V2)"):
                with open(PROJECT_DIR / "data" / "kyc_and_compliance.txt", "r", encoding="utf-8") as f:
                    st.text(f.read())

    col3, col4 = st.columns(2)
    with col3:
        with st.expander("📄 Loan Terms & Deposit Rates (AGB-LND-2026-Q1)"):
            with open(PROJECT_DIR / "data" / "loan_and_interest_terms.txt", "r", encoding="utf-8") as f:
                st.text(f.read())
        with col4:
            with st.expander("📄 Fee Schedule & Service Charges (AGB-FEE-2026-V1)"):
                with open(PROJECT_DIR / "data" / "fee_schedule.txt", "r", encoding="utf-8") as f:
                    st.text(f.read())


with tab_audit:
    st.subheader("🔒 PII-Sanitized Telemetry & Security Audit Logs")
    st.caption("Live stream from logs/telemetry_audit.log. Notice that all card numbers, phone numbers, and account IDs are automatically redacted.")
    
    log_file = PROJECT_DIR / "logs" / "telemetry_audit.log"
    if log_file.exists():
        with open(log_file, "r", encoding="utf-8") as f:
            log_lines = f.readlines()
        st.code("".join(log_lines[-25:]), language="json")
    else:
        st.info("No audit logs recorded yet. Send a query to generate telemetry.")


# ==============================================================================
# CHAT INPUT — Placed at the ROOT LEVEL (Native Streamlit fixed bottom dock)
# ==============================================================================
if prompt := st.chat_input("Ask about account balance, calculate EMI, check FD rates, or report an issue..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("Processing inquiry through cognitive pipeline..."):
        res = agent.process_query(prompt)
        
    st.session_state.messages.append({
        "role": "assistant",
        "content": res["response"],
        "meta": {
            "plan": res["plan"],
            "tools": res["tools_used"],
            "sources": res["sources"],
            "risk": res["risk_flag"],
            "latency": res["latency_sec"]
        }
    })
    st.rerun()
