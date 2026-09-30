"""
================================================================================
APEX GLOBAL BANK — RAG & VECTOR SEARCH ENGINE (rag_engine.py)
================================================================================
Phase 4: Add Knowledge & Retrieval
Loads banking policy corpus, generates OpenAI dense embeddings, builds a FAISS
vector index, and retrieves top-k relevant grounded context for user inquiries.
================================================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
VECTORSTORE_DIR = PROJECT_DIR / "vectorstore"


def get_embeddings_client():
    """Initializes the OpenAI Embeddings client using .env settings."""
    load_dotenv(PROJECT_DIR / ".env")
    api_key = os.environ.get("OPENAI_API_KEY")
    api_base = os.environ.get("OPENAI_API_BASE")
    
    kwargs = {"model": "text-embedding-3-small", "openai_api_key": api_key}
    if api_base:
        kwargs["openai_api_base"] = api_base
    return OpenAIEmbeddings(**kwargs)


def build_or_load_vector_index(force_rebuild: bool = False):
    """
    Builds the FAISS vector index from documents in data/ or loads from disk if already cached.
    """
    index_file = VECTORSTORE_DIR / "index.faiss"
    embeddings = get_embeddings_client()

    if index_file.exists() and not force_rebuild:
        vectorstore = FAISS.load_local(
            str(VECTORSTORE_DIR),
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vectorstore

    # Load all documents from data/
    doc_files = list(DATA_DIR.glob("*.txt"))
    if not doc_files:
        raise FileNotFoundError(f"No .txt documents found in {DATA_DIR}")

    raw_docs = []
    for f in doc_files:
        loader = TextLoader(str(f), encoding="utf-8")
        loaded = loader.load()
        for d in loaded:
            d.metadata["source"] = f.name
        raw_docs.extend(loaded)

    # Chunking: 800 characters with 150 overlap for banking policy clauses
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", "1.", "2.", "3.", " ", ""]
    )
    chunks = splitter.split_documents(raw_docs)

    vectorstore = FAISS.from_documents(chunks, embeddings)
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(VECTORSTORE_DIR))
    
    return vectorstore


def retrieve_context(query: str, top_k: int = 3) -> tuple[str, list]:
    """
    Retrieves the top-k most semantically relevant text chunks from the banking knowledge base.
    Returns: (concatenated_context_str, list_of_source_metadata)
    """
    vs = build_or_load_vector_index()
    results = vs.similarity_search(query, k=top_k)
    
    context_blocks = []
    sources = []
    for idx, doc in enumerate(results, 1):
        src = doc.metadata.get("source", "Knowledge Base")
        sources.append(src)
        context_blocks.append(f"[Document: {src} | Chunk {idx}]\n{doc.page_content.strip()}")
        
    combined_context = "\n\n".join(context_blocks)
    return combined_context, list(set(sources))

