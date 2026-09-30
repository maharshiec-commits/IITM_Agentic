import os
from typing import Tuple

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from app.config import settings
from app.rag.store import store_manager

def ingest_folder(folder: str, index_path: str) -> Tuple[int, int, int]:
    """
    Returns: (pdf_files, loaded_pages, chunks_created)
    """
    if not os.path.isdir(folder):
        raise ValueError(f"Folder not found: {folder}")

    pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    if not pdf_files:
        raise ValueError(f"No PDF files found in folder: {folder}")

    documents = []
    for file in pdf_files:
        loader = PyPDFLoader(os.path.join(folder, file))
        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_documents(documents)

    embeddings = store_manager._embeddings()  # uses same config/keys/base_url
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(index_path)

    # ensure queries load fresh index
    store_manager.invalidate()

    return len(pdf_files), len(documents), len(chunks)