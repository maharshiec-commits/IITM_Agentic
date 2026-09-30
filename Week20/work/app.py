"""
================================================================================
ORNATIVA JEWELS — VISUAL CHATBOT APPLICATION (app.py)
================================================================================
Week 20: Graded Mini Project
Brand: Ornativa Jewels (Hyderabad, India)
Dataset: Jewellery Details.pdf
Framework: Interactive Streamlit Visual Interface for the RAG Flow
================================================================================
"""

import os
import sys
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

from test_flow import build_pipeline, setup_environment, load_catalogue

st.set_page_config(
    page_title="Ornativa Jewels — Virtual Jewellery Assistant",
    page_icon="💎",
    layout="wide",
)

# Custom Styling
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #d4af37; margin-bottom: 0px; }
    .sub-title { font-size: 1.05rem; color: #c5a059; margin-bottom: 1.2rem; }
    .product-card { background-color: #1e1e2e; border: 1px solid #313244; border-radius: 8px; padding: 12px; margin-bottom: 8px; }
    .badge-available { background-color: #2e7d32; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; }
    .badge-out { background-color: #c62828; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_chatbot_chain():
    """Initializes the RAG chain and FAISS vector index."""
    api_key, api_base, model = setup_environment()
    chain, vectorstore = build_pipeline(api_key, api_base, model)
    return chain, vectorstore


# Sidebar: Brand details, Visual Pipeline & Catalogue Inspector
with st.sidebar:
    st.markdown("### 💎 Ornativa Jewels")
    st.markdown("*Flagship Store: Jubilee Hills, Hyderabad, India*")
    st.divider()

    st.subheader("Visual Pipeline Flow")
    st.markdown("""
    ```
    ┌───────────────────────────┐
    │  Jewellery Details.pdf    │ (File Loader)
    └─────────────┬─────────────┘
                  ▼
    ┌───────────────────────────┐
    │  SplitText (1000 / 200)   │ (Text Splitter)
    └─────────────┬─────────────┘
                  ▼
    ┌───────────────────────────┐
    │  OpenAI Embeddings        │ (text-embedding-3-small)
    └─────────────┬─────────────┘
                  ▼
    ┌───────────────────────────┐
    │  Vector Store (FAISS)     │ ◄── [Top-K = 4]
    └─────────────┬─────────────┘
                  ▼
    ┌───────────────────────────┐
    │  Buffer Memory            │ ◄── Multi-Turn History
    └─────────────┬─────────────┘
                  ▼
    ┌───────────────────────────┐
    │  Ornativa Prompt Template │ ◄── Out-of-Stock Fallback
    └─────────────┬─────────────┘
                  ▼
    ┌───────────────────────────┐
    │  Chat Model (gpt-4o-mini) │ ──► Output Response
    └───────────────────────────┘
    ```
    """)
    st.divider()

    st.subheader("Sample Test Inquiries")
    sample_queries = [
        "List all available diamond items.",
        "What is the price of the Pearl Necklace?",
        "Which products are made of 22K gold?",
        "Show me diamond products.",
        "What's the price of the ring?",
        "I want to buy the Ruby Solitaire Ring. Is it in stock?",
        "Can I purchase the Emerald Cuff Bracelet?",
        "Do you sell silver anklets?"
    ]
    for q in sample_queries:
        if st.button(q, key=f"btn_{q}", use_container_width=True):
            st.session_state.pending_query = q

    st.divider()
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        if "chain" in st.session_state and st.session_state.chain:
            st.session_state.chain.memory.clear()
        st.rerun()


# Initialize chain
if "chain" not in st.session_state:
    with st.spinner("Initializing visual RAG pipeline and vector store..."):
        chain, vs = get_chatbot_chain()
        st.session_state.chain = chain
        st.session_state.vectorstore = vs

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! Welcome to Ornativa Jewels, Hyderabad. I am your virtual jewellery assistant. How may I assist you with our rings, necklaces, earrings, bracelets, and pendants today?"}
    ]

# Handle button query from sidebar if clicked
if "pending_query" in st.session_state:
    user_input = st.session_state.pop("pending_query")
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Consulting jewellery catalogue..."):
        res = st.session_state.chain.invoke({"question": user_input})
        ans = res["answer"]
        srcs = list(set([d.metadata.get("source", "Jewellery Details.pdf") for d in res["source_documents"]]))
    st.session_state.messages.append({"role": "assistant", "content": ans, "sources": srcs})
    st.rerun()

# Main View: Tabs
tab_chat, tab_catalogue, tab_architecture = st.tabs(["💬 Customer Chatbot", "📖 Catalogue Inventory", "📐 Architecture & Nodes"])

with tab_chat:
    st.markdown('<div class="main-title">Ornativa Jewels — Virtual Jewellery Expert</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Welcome to Ornativa Jewels, Hyderabad. Experience our bespoke fine jewellery collection.</div>', unsafe_allow_html=True)

    # Render all conversation messages inside the chat tab
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("📄 Source Citation"):
                    for s in msg["sources"]:
                        st.caption(f"• Document: `{s}`")


with tab_catalogue:
    st.subheader("Official Product Catalogue — Jewellery Details.pdf")
    st.markdown("All 10 items indexed in the local vector database:")

    products = [
        {"id": "R101", "name": "Classic Diamond Ring", "cat": "Ring", "mat": "18K Gold + Diamond", "wt": "5.2 g", "price": "₹1,35,000", "stock": "Available"},
        {"id": "R102", "name": "Ruby Solitaire Ring", "cat": "Ring", "mat": "22K Gold + Ruby", "wt": "4.8 g", "price": "₹98,500", "stock": "Out of Stock"},
        {"id": "N201", "name": "Pearl Necklace", "cat": "Necklace", "mat": "18K Gold + Pearl", "wt": "28.5 g", "price": "₹2,45,000", "stock": "Available"},
        {"id": "N202", "name": "Emerald Choker", "cat": "Necklace", "mat": "22K Gold + Emerald", "wt": "32.0 g", "price": "₹3,10,000", "stock": "Available"},
        {"id": "E301", "name": "Daily Wear Gold Earrings", "cat": "Earrings", "mat": "22K Gold", "wt": "7.5 g", "price": "₹55,000", "stock": "Available"},
        {"id": "E302", "name": "Diamond Stud Earrings", "cat": "Earrings", "mat": "18K Gold + Diamond", "wt": "6.2 g", "price": "₹1,05,000", "stock": "Available"},
        {"id": "B401", "name": "Gold Chain Bracelet", "cat": "Bracelet", "mat": "22K Gold", "wt": "12.0 g", "price": "₹87,500", "stock": "Available"},
        {"id": "B402", "name": "Emerald Cuff Bracelet", "cat": "Bracelet", "mat": "18K Gold + Emerald", "wt": "15.0 g", "price": "₹1,50,000", "stock": "Out of Stock"},
        {"id": "P501", "name": "Lotus Pendant", "cat": "Pendant", "mat": "18K Gold + Diamond", "wt": "8.0 g", "price": "₹72,000", "stock": "Available"},
        {"id": "P502", "name": "Om Symbol Pendant", "cat": "Pendant", "mat": "22K Gold", "wt": "6.5 g", "price": "₹48,000", "stock": "Available"},
    ]

    col1, col2 = st.columns(2)
    for i, p in enumerate(products):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            badge_class = "badge-available" if p["stock"] == "Available" else "badge-out"
            st.markdown(f"""
            <div class="product-card">
                <b>[{p['id']}] {p['name']}</b> &nbsp; <span class="{badge_class}">{p['stock']}</span><br>
                <small><b>Category:</b> {p['cat']} | <b>Material:</b> {p['mat']} | <b>Weight:</b> {p['wt']}</small><br>
                <span style="color:#d4af37; font-weight:bold;">Price: {p['price']}</span>
            </div>
            """, unsafe_allow_html=True)


with tab_architecture:
    st.subheader("Visual Pipeline Architecture (Langflow & Flowise Specification)")
    st.markdown("""
    ### Component & Node Wiring
    1. **Document Loader Node (`File` / `pdfFile`)**: Ingests `Jewellery Details.pdf`
    2. **Text Splitter Node (`SplitText` / `RecursiveCharacterTextSplitter`)**: 
       - Chunk size: `1000` characters
       - Chunk overlap: `200` characters
       - *Rationale*: Preserves entire product specifications without splitting individual product records.
    3. **Embeddings Node (`OpenAIEmbeddings`)**: Generates vectors using `text-embedding-3-small`
    4. **Vector Store Node (`Chroma` / `FAISS`)**: Indexes embeddings with similarity search (`top_k = 4`)
    5. **Memory Node (`ChatMemory` / `BufferMemory`)**: Window of 6 turns to resolve follow-ups (e.g., *"What is the price of the ring?"*)
    6. **Prompt Node (`Prompt Template`)**: Enforces Ornativa Jewels brand persona (polite, concise, factual) and automatic alternative recommendation for out-of-stock items.
    7. **Chat Model Node (`OpenAIModel` / `ChatOpenAI`)**: Uses `gpt-4o-mini` with temperature `0.1` for factual fidelity.

    ### Exported Flow Files
    - [`ornativa_jewels_langflow.json`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week20/work/ornativa_jewels_langflow.json) — Import into Langflow
    - [`ornativa_jewels_flowise.json`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week20/work/ornativa_jewels_flowise.json) — Import into Flowise
    """)


# ==============================================================================
# CHAT INPUT — Placed at the ROOT LEVEL so it always sticks to the screen bottom!
# ==============================================================================
if prompt := st.chat_input("Ask about diamond items, 22K gold, pricing, or product availability..."):
    # Append user question
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Query RAG chain
    with st.spinner("Consulting jewellery catalogue..."):
        res = st.session_state.chain.invoke({"question": prompt})
        ans = res["answer"]
        srcs = list(set([d.metadata.get("source", "Jewellery Details.pdf") for d in res["source_documents"]]))
    
    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": ans, "sources": srcs})
    
    # Rerun to cleanly display updated conversation
    st.rerun()
