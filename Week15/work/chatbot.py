"""
================================================================================
RAG CHATBOT WITH CONVERSATION HISTORY (chatbot.py)
================================================================================
Week 15: RAG Conversational Assistant
Domain: E-Commerce (ShopEase) — Product Policies & Customer Support

This module:
  1. Loads the FAISS vector store created by ingest.py
  2. Sets up a conversational RAG chain with memory
  3. Retrieves relevant document chunks per query
  4. Generates grounded answers with source citations
  5. Supports follow-up questions using conversation history
  6. Refuses to answer when information is not in the documents
================================================================================
"""

import os
import sys
from pathlib import Path

# Ensure UTF-8 stdout encoding on Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from dotenv import load_dotenv

# LangChain imports
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.prompts.chat import ChatPromptTemplate


# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
PROJECT_DIR = Path(__file__).parent
VECTORSTORE_DIR = PROJECT_DIR / "vectorstore"

# Retrieval configuration
TOP_K = 4               # Number of chunks to retrieve per query
MEMORY_WINDOW = 8       # Number of conversation turns to remember

# System prompt that enforces grounding and prevents hallucination
SYSTEM_PROMPT = """You are ShopEase Support Assistant, a helpful and accurate customer support chatbot for ShopEase E-Commerce.

STRICT RULES:
1. Answer ONLY based on the provided context documents. Do NOT use your general knowledge.
2. If the answer is not found in the provided context, respond with: "I don't have enough information in the provided documents to answer that question. Please contact our support team at 1800-SHOP-EASE for further assistance."
3. When answering, cite the specific policy or document section (e.g., "According to our Return Policy (Section 4.1)...").
4. Be professional, helpful, and empathetic.
5. For follow-up questions, use the conversation history to maintain context.
6. If the question is ambiguous, ask for clarification.
7. Provide specific details like timelines, costs, and steps when available in the documents.
8. Never promise anything that is not explicitly stated in the policy documents.

CONTEXT FROM DOCUMENTS:
{context}
"""

CONDENSE_PROMPT = """Given the following conversation history and a follow-up question, rephrase the follow-up question to be a standalone question that captures the full context.

Chat History:
{chat_history}

Follow-up Question: {question}

Standalone Question:"""


# ──────────────────────────────────────────────────────────────────────────────
# ENVIRONMENT SETUP
# ──────────────────────────────────────────────────────────────────────────────
def setup_environment():
    """Load environment variables and validate."""
    load_dotenv(PROJECT_DIR / ".env")

    api_key = os.environ.get("OPENAI_API_KEY")
    api_base = os.environ.get("OPENAI_API_BASE")
    model = os.environ.get("MODEL", "gpt-4o-mini")

    if not api_key:
        print("ERROR: OPENAI_API_KEY not found. Add it to .env file.")
        sys.exit(1)

    return api_key, api_base, model


# ──────────────────────────────────────────────────────────────────────────────
# LOAD VECTOR STORE
# ──────────────────────────────────────────────────────────────────────────────
def load_vector_store(api_key, api_base=None):
    """Load the FAISS vector store from disk."""
    if not VECTORSTORE_DIR.exists() or not list(VECTORSTORE_DIR.iterdir()):
        print("ERROR: Vector store not found. Run ingest.py first.")
        print("  python ingest.py")
        sys.exit(1)

    embedding_kwargs = {
        "model": "text-embedding-3-small",
        "openai_api_key": api_key,
    }
    if api_base:
        embedding_kwargs["openai_api_base"] = api_base

    embeddings = OpenAIEmbeddings(**embedding_kwargs)

    vectorstore = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    print(f"[OK] Vector store loaded: {vectorstore.index.ntotal} vectors")
    return vectorstore


# ──────────────────────────────────────────────────────────────────────────────
# BUILD RAG CHAIN
# ──────────────────────────────────────────────────────────────────────────────
def build_rag_chain(vectorstore, api_key, api_base=None, model="gpt-4o-mini"):
    """Build the conversational RAG chain with memory."""

    # LLM configuration
    llm_kwargs = {
        "model": model,
        "temperature": 0.1,  # Low temperature for factual accuracy
        "openai_api_key": api_key,
    }
    if api_base:
        llm_kwargs["openai_api_base"] = api_base

    llm = ChatOpenAI(**llm_kwargs)

    # Retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )

    # Conversation memory
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
        k=MEMORY_WINDOW,
    )

    # Condense question prompt (for follow-ups)
    condense_prompt = PromptTemplate.from_template(CONDENSE_PROMPT)

    # QA prompt with system instructions
    qa_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template("{question}"),
    ])

    # Build the chain
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        condense_question_prompt=condense_prompt,
        combine_docs_chain_kwargs={"prompt": qa_prompt},
        return_source_documents=True,
        verbose=False,
    )

    print(f"[OK] RAG chain built: model={model}, top_k={TOP_K}, memory={MEMORY_WINDOW} turns")
    return chain


# ──────────────────────────────────────────────────────────────────────────────
# CHAT FUNCTION
# ──────────────────────────────────────────────────────────────────────────────
def chat(chain, user_query: str) -> dict:
    """
    Send a query through the RAG chain.

    Returns:
        dict with 'answer', 'sources' (list of source docs), and 'source_names'
    """
    result = chain.invoke({"question": user_query})

    answer = result.get("answer", "")
    source_docs = result.get("source_documents", [])

    # Extract unique source file names
    source_names = list(set(
        doc.metadata.get("source", "unknown")
        for doc in source_docs
    ))

    return {
        "answer": answer,
        "sources": source_docs,
        "source_names": source_names,
    }


def format_response(result: dict, show_sources: bool = True) -> str:
    """Format the chatbot response with optional source citations."""
    output_parts = [result["answer"]]

    if show_sources and result["source_names"]:
        output_parts.append("\n--- Sources ---")
        for name in result["source_names"]:
            output_parts.append(f"  - {name}")

    return "\n".join(output_parts)


# ──────────────────────────────────────────────────────────────────────────────
# INTERACTIVE CLI CHATBOT
# ──────────────────────────────────────────────────────────────────────────────
def run_interactive_chat():
    """Run the chatbot in interactive command-line mode."""
    print("=" * 70)
    print("  ShopEase Support Assistant (RAG Chatbot)")
    print("  Domain: E-Commerce Customer Support")
    print("  Type 'quit' or 'exit' to end the conversation")
    print("  Type 'clear' to reset conversation history")
    print("=" * 70)

    # Setup
    api_key, api_base, model = setup_environment()
    vectorstore = load_vector_store(api_key, api_base)
    chain = build_rag_chain(vectorstore, api_key, api_base, model)

    print("\nReady! Ask me anything about ShopEase policies.\n")

    conversation_log = []  # For saving sample conversations

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye! Thank you for using ShopEase Support.")
            break
        if user_input.lower() == "clear":
            chain.memory.clear()
            print("[Memory cleared. Starting fresh conversation.]\n")
            continue

        # Get response
        result = chat(chain, user_input)
        formatted = format_response(result, show_sources=True)

        print(f"\nAssistant: {formatted}\n")

        # Log conversation
        conversation_log.append({
            "user": user_input,
            "assistant": result["answer"],
            "sources": result["source_names"],
        })

    # Save conversation log
    if conversation_log:
        save_conversation_log(conversation_log)


def save_conversation_log(log: list):
    """Save the conversation log to a file."""
    log_file = PROJECT_DIR / "sample_conversation_log.txt"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("  SAMPLE CONVERSATION LOG\n")
        f.write("  ShopEase Support Assistant (RAG Chatbot)\n")
        f.write("=" * 70 + "\n\n")

        for i, entry in enumerate(log, 1):
            f.write(f"--- Turn {i} ---\n")
            f.write(f"User: {entry['user']}\n\n")
            f.write(f"Assistant: {entry['assistant']}\n")
            if entry['sources']:
                f.write(f"Sources: {', '.join(entry['sources'])}\n")
            f.write("\n")

    print(f"\n[Conversation log saved to: {log_file}]")


# ──────────────────────────────────────────────────────────────────────────────
# DEMO MODE — Run preset queries for evaluation/grading
# ──────────────────────────────────────────────────────────────────────────────
def run_demo():
    """Run a preset demonstration with sample queries showing all capabilities."""
    print("=" * 70)
    print("  ShopEase Support Assistant — DEMO MODE")
    print("  Running preset sample queries for evaluation")
    print("=" * 70)

    api_key, api_base, model = setup_environment()
    vectorstore = load_vector_store(api_key, api_base)
    chain = build_rag_chain(vectorstore, api_key, api_base, model)

    # Demo queries that demonstrate all required capabilities
    demo_queries = [
        # 1. Direct policy question
        "What is ShopEase's return policy for electronics?",
        # 2. Follow-up question (uses conversation history)
        "What if the electronics item arrived damaged?",
        # 3. Another follow-up
        "How long do I have to report the damage?",
        # 4. New topic — shipping
        "What are the shipping options and their costs?",
        # 5. Follow-up on shipping
        "Is same-day delivery available in Pune?",
        # 6. Warranty question
        "What does the ShopEase Protect+ Complete plan cover?",
        # 7. Payment question
        "Can I pay using EMI? What's the minimum order value?",
        # 8. Membership question
        "What are the benefits of ShopEase Prime membership?",
        # 9. Follow-up on membership
        "What about the student plan pricing?",
        # 10. Out-of-scope question (should refuse)
        "What is the weather forecast for tomorrow in Mumbai?",
    ]

    conversation_log = []

    for i, query in enumerate(demo_queries, 1):
        print(f"\n{'-' * 60}")
        print(f"  Query {i}: {query}")
        print(f"{'-' * 60}")

        result = chat(chain, query)
        formatted = format_response(result, show_sources=True)
        print(f"\n  Assistant: {formatted}")

        conversation_log.append({
            "user": query,
            "assistant": result["answer"],
            "sources": result["source_names"],
        })

    # Save demo log
    save_conversation_log(conversation_log)

    print("\n" + "=" * 70)
    print("  DEMO COMPLETE!")
    print(f"  {len(demo_queries)} queries processed successfully")
    print("  Conversation log saved to: sample_conversation_log.txt")
    print("=" * 70)


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    else:
        run_interactive_chat()

