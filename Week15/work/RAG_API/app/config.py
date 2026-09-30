import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_api_base: str | None = os.getenv("OPENAI_API_BASE")  # optional

    default_index_path: str = os.getenv("RAG_DEFAULT_INDEX_PATH", "hr_faiss_index")
    chunk_size: int = int(os.getenv("RAG_DEFAULT_CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("RAG_DEFAULT_CHUNK_OVERLAP", "150"))
    default_k: int = int(os.getenv("RAG_DEFAULT_K", "4"))

    llm_model: str = os.getenv("RAG_LLM_MODEL", "gpt-4o-mini")
    embed_model: str = os.getenv("RAG_EMBED_MODEL", "text-embedding-3-small")

    # add near other settings
    enable_sanitization: bool = os.getenv("RAG_ENABLE_SANITIZATION", "true").lower() == "true"
    sanitize_context: bool = os.getenv("RAG_SANITIZE_CONTEXT", "true").lower() == "true"

settings = Settings()