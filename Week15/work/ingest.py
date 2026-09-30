"""
================================================================================
DOCUMENT INGESTION & INDEXING (ingest.py)
================================================================================
Week 15: RAG Conversational Assistant
Domain: E-Commerce (ShopEase) — Product Policies & Customer Support

This module:
  1. Loads .txt and .pdf documents from the documents/ folder
  2. Splits content into semantic chunks using RecursiveCharacterTextSplitter
  3. Generates embeddings using OpenAI embeddings API
  4. Stores embeddings in a FAISS vector store for retrieval
================================================================================
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# LangChain imports
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
PROJECT_DIR = Path(__file__).parent
DOCUMENTS_DIR = PROJECT_DIR / "documents"
VECTORSTORE_DIR = PROJECT_DIR / "vectorstore"

# Chunking parameters — tuned for policy documents
CHUNK_SIZE = 800       # Characters per chunk
CHUNK_OVERLAP = 150    # Overlap between chunks for context continuity
SEPARATORS = ["\n\n", "\n", ". ", " ", ""]  # Prefer splitting at paragraphs/sections


def setup_environment():
    """Load environment variables and validate API key."""
    load_dotenv(PROJECT_DIR / ".env")

    api_key = os.environ.get("OPENAI_API_KEY")
    api_base = os.environ.get("OPENAI_API_BASE")

    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in .env file.")
        print("Please add your API key to the .env file:")
        print('  OPENAI_API_KEY="your-key-here"')
        sys.exit(1)

    print(f"[CONFIG] API Key: ...{api_key[-8:]}")
    if api_base:
        print(f"[CONFIG] API Base: {api_base}")
    
    return api_key, api_base


# ──────────────────────────────────────────────────────────────────────────────
# STEP 1: LOAD DOCUMENTS
# ──────────────────────────────────────────────────────────────────────────────
def load_documents():
    """Load all .txt documents from the documents/ folder."""
    if not DOCUMENTS_DIR.exists():
        print(f"ERROR: Documents directory not found: {DOCUMENTS_DIR}")
        sys.exit(1)

    txt_files = list(DOCUMENTS_DIR.glob("*.txt"))
    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))
    all_files = txt_files + pdf_files

    if not all_files:
        print(f"ERROR: No .txt or .pdf files found in {DOCUMENTS_DIR}")
        sys.exit(1)

    print(f"\n[STEP 1] Loading documents from: {DOCUMENTS_DIR}")
    print(f"  Found {len(txt_files)} TXT files, {len(pdf_files)} PDF files")

    all_docs = []

    # Load TXT files
    for txt_file in txt_files:
        try:
            loader = TextLoader(str(txt_file), encoding="utf-8")
            docs = loader.load()
            # Add source metadata
            for doc in docs:
                doc.metadata["source"] = txt_file.name
                doc.metadata["file_type"] = "txt"
            all_docs.extend(docs)
            print(f"  Loaded: {txt_file.name} ({len(docs[0].page_content)} chars)")
        except Exception as e:
            print(f"  WARNING: Failed to load {txt_file.name}: {e}")

    # Load PDF files (if any)
    for pdf_file in pdf_files:
        try:
            from langchain_community.document_loaders import PyPDFLoader
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = pdf_file.name
                doc.metadata["file_type"] = "pdf"
            all_docs.extend(docs)
            print(f"  Loaded: {pdf_file.name} ({len(docs)} pages)")
        except ImportError:
            print(f"  WARNING: PyPDF not installed. Skipping {pdf_file.name}")
            print("  Install with: pip install pypdf")
        except Exception as e:
            print(f"  WARNING: Failed to load {pdf_file.name}: {e}")

    print(f"  Total documents loaded: {len(all_docs)}")
    return all_docs


# ──────────────────────────────────────────────────────────────────────────────
# STEP 2: SPLIT INTO CHUNKS
# ──────────────────────────────────────────────────────────────────────────────
def split_documents(documents):
    """Split documents into semantic chunks for embedding."""
    print(f"\n[STEP 2] Splitting documents into chunks")
    print(f"  Chunk size: {CHUNK_SIZE} chars, Overlap: {CHUNK_OVERLAP} chars")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(documents)

    print(f"  Total chunks created: {len(chunks)}")

    # Show sample chunks
    print(f"\n  Sample chunk (first):")
    print(f"    Source: {chunks[0].metadata.get('source', 'unknown')}")
    print(f"    Content: {chunks[0].page_content[:120]}...")
    print(f"    Length: {len(chunks[0].page_content)} chars")

    return chunks


# ──────────────────────────────────────────────────────────────────────────────
# STEP 3: GENERATE EMBEDDINGS & BUILD VECTOR STORE
# ──────────────────────────────────────────────────────────────────────────────
def create_vector_store(chunks, api_key, api_base=None):
    """Generate OpenAI embeddings and store in FAISS vector store."""
    print(f"\n[STEP 3] Generating embeddings and building FAISS vector store")

    # Configure embeddings
    embedding_kwargs = {
        "model": "text-embedding-3-small",
        "openai_api_key": api_key,
    }
    if api_base:
        embedding_kwargs["openai_api_base"] = api_base

    embeddings = OpenAIEmbeddings(**embedding_kwargs)

    print(f"  Embedding model: text-embedding-3-small")
    print(f"  Processing {len(chunks)} chunks...")

    # Build FAISS index from chunks
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    print(f"  FAISS index built successfully!")
    print(f"  Index size: {vectorstore.index.ntotal} vectors")

    return vectorstore


# ──────────────────────────────────────────────────────────────────────────────
# STEP 4: SAVE VECTOR STORE TO DISK
# ──────────────────────────────────────────────────────────────────────────────
def save_vector_store(vectorstore):
    """Save the FAISS vector store to disk for later retrieval."""
    print(f"\n[STEP 4] Saving vector store to: {VECTORSTORE_DIR}")

    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(VECTORSTORE_DIR))

    # Verify saved files
    saved_files = list(VECTORSTORE_DIR.iterdir())
    print(f"  Saved files: {[f.name for f in saved_files]}")
    total_size = sum(f.stat().st_size for f in saved_files if f.is_file())
    print(f"  Total size: {total_size / 1024:.1f} KB")
    print(f"  Vector store saved successfully!")


# ──────────────────────────────────────────────────────────────────────────────
# STEP 5: VERIFICATION — TEST RETRIEVAL
# ──────────────────────────────────────────────────────────────────────────────
def verify_retrieval(vectorstore):
    """Run a test query to verify the retrieval pipeline works."""
    print(f"\n[STEP 5] Verification — Testing retrieval")

    test_queries = [
        "What is the return policy for electronics?",
        "How much does same-day delivery cost?",
        "What does the warranty cover?",
    ]

    for query in test_queries:
        results = vectorstore.similarity_search(query, k=2)
        print(f"\n  Query: \"{query}\"")
        for i, doc in enumerate(results):
            source = doc.metadata.get("source", "unknown")
            preview = doc.page_content[:100].replace("\n", " ")
            print(f"    [{i+1}] Source: {source} | \"{preview}...\"")


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("  DOCUMENT INGESTION & INDEXING PIPELINE")
    print("  Domain: E-Commerce (ShopEase) Customer Support")
    print("=" * 70)

    # Setup
    api_key, api_base = setup_environment()

    # Pipeline
    documents = load_documents()
    chunks = split_documents(documents)
    vectorstore = create_vector_store(chunks, api_key, api_base)
    save_vector_store(vectorstore)
    verify_retrieval(vectorstore)

    print("\n" + "=" * 70)
    print("  INGESTION COMPLETE!")
    print(f"  Documents: {len(documents)} | Chunks: {len(chunks)} | Vectors: {vectorstore.index.ntotal}")
    print("  Vector store saved to: vectorstore/")
    print("  Ready for chatbot.py")
    print("=" * 70)


if __name__ == "__main__":
    main()

