"""
================================================================================
STREAMLIT UI FOR RAG CHATBOT (app.py) — Bonus Deliverable
================================================================================
Streamlit-based web interface for the ShopEase Support Assistant.
Run with: streamlit run app.py
================================================================================
"""

import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Add project directory to path
PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

from chatbot import load_vector_store, build_rag_chain, chat


# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ShopEase Support Assistant",
    page_icon="🛒",
    layout="wide",
)


# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ──────────────────────────────────────────────────────────────────────────────
if "chain" not in st.session_state:
    st.session_state.chain = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initialized" not in st.session_state:
    st.session_state.initialized = False


# ──────────────────────────────────────────────────────────────────────────────
# INITIALIZATION
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def initialize_chatbot():
    """Initialize the RAG chain (cached to avoid reloading)."""
    load_dotenv(PROJECT_DIR / ".env")
    
    api_key = os.environ.get("OPENAI_API_KEY")
    api_base = os.environ.get("OPENAI_API_BASE")
    model = os.environ.get("MODEL", "gpt-4o-mini")
    
    if not api_key:
        st.error("OPENAI_API_KEY not found. Please add it to your .env file.")
        st.stop()
    
    vectorstore = load_vector_store(api_key, api_base)
    chain = build_rag_chain(vectorstore, api_key, api_base, model)
    return chain


# ──────────────────────────────────────────────────────────────────────────────
# UI LAYOUT
# ──────────────────────────────────────────────────────────────────────────────
# Header
st.title("🛒 ShopEase Support Assistant")
st.caption("RAG-powered E-Commerce Customer Support Chatbot | Week 15 Mini Project")

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This chatbot answers questions about **ShopEase E-Commerce** policies using 
    Retrieval-Augmented Generation (RAG).
    
    **Documents indexed:**
    - Return & Refund Policy
    - Shipping & Delivery Policy  
    - Product Warranty Policy
    - Payment Methods & FAQs
    - Prime Membership Program
    """)
    
    st.divider()
    
    st.subheader("Sample Questions")
    sample_questions = [
        "What is the return policy for electronics?",
        "How much does same-day delivery cost?",
        "What does the warranty cover?",
        "Can I pay using EMI?",
        "What are Prime membership benefits?",
    ]
    for q in sample_questions:
        if st.button(q, key=q, use_container_width=True):
            st.session_state.sample_query = q
    
    st.divider()
    
    if st.button("Clear Conversation", type="secondary", use_container_width=True):
        st.session_state.messages = []
        if st.session_state.chain:
            st.session_state.chain.memory.clear()
        st.rerun()
    
    st.divider()
    show_sources = st.checkbox("Show source documents", value=True)


# Initialize chatbot
if not st.session_state.initialized:
    with st.spinner("Loading knowledge base..."):
        st.session_state.chain = initialize_chatbot()
        st.session_state.initialized = True
    st.success("Knowledge base loaded! Ask me anything about ShopEase policies.")


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and show_sources and message.get("sources"):
            with st.expander("📄 Source Documents"):
                for source in message["sources"]:
                    st.caption(f"• {source}")


# Handle sample query from sidebar
if "sample_query" in st.session_state:
    user_input = st.session_state.pop("sample_query")
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            result = chat(st.session_state.chain, user_input)
        st.markdown(result["answer"])
        if show_sources and result["source_names"]:
            with st.expander("📄 Source Documents"):
                for source in result["source_names"]:
                    st.caption(f"• {source}")
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["source_names"],
    })
    st.rerun()


# Chat input
if user_input := st.chat_input("Ask about return policies, shipping, warranty, payments, or membership..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            result = chat(st.session_state.chain, user_input)
        st.markdown(result["answer"])
        if show_sources and result["source_names"]:
            with st.expander("📄 Source Documents"):
                for source in result["source_names"]:
                    st.caption(f"• {source}")
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["source_names"],
    })
    st.rerun()
