import os
import threading
from typing import Optional

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.config import settings

class VectorStoreManager:
    """
    Loads/saves FAISS index on disk and caches it in memory for queries.
    Thread-safe for basic usage.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._vectorstore: Optional[FAISS] = None
        self._index_path: Optional[str] = None

    def _embeddings(self) -> OpenAIEmbeddings:
        # Mirrors your current setup; supports optional base_url
        kwargs = {"model": settings.embed_model}
        if settings.openai_api_base:
            kwargs["base_url"] = settings.openai_api_base
        if settings.openai_api_key:
            kwargs["openai_api_key"] = settings.openai_api_key
        return OpenAIEmbeddings(**kwargs)

    def load(self, index_path: str) -> FAISS:
        with self._lock:
            if self._vectorstore is not None and self._index_path == index_path:
                return self._vectorstore

            embeddings = self._embeddings()
            vs = FAISS.load_local(
                index_path,
                embeddings,
                allow_dangerous_deserialization=True,
            )
            self._vectorstore = vs
            self._index_path = index_path
            return vs

    def invalidate(self) -> None:
        with self._lock:
            self._vectorstore = None
            self._index_path = None

store_manager = VectorStoreManager()