import os
import time
import logging
from fastapi import FastAPI, HTTPException

from app.config import settings
from app.schemas import IngestRequest, IngestResponse, QueryRequest, QueryResponse, SourceChunk
from app.logging_config import setup_logging
from app.rag.ingest import ingest_folder
from app.rag.query import answer_query
from app.privacy import mask_private_data
from app.safety import safety_wrapper


setup_logging()
logger = logging.getLogger("fastapi_rag")

app = FastAPI(title="FastAPI RAG Service", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/env")
def env_check():
    # minimal check; we’ll expand in Task 12 with richer reporting
    required = {
        "OPENAI_API_KEY": bool(settings.openai_api_key),
    }
    optional = {
        "OPENAI_API_BASE": bool(settings.openai_api_base),
    }
    ok = all(required.values())
    return {"ok": ok, "required": required, "optional": optional}


@app.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest):
    index_path = req.index_path or settings.default_index_path

    t0 = time.perf_counter()
    logger.info(f"/ingest called | folder={req.folder} | index_path={index_path}")

    try:
        pdf_files, loaded_pages, chunks_created = ingest_folder(req.folder, index_path)
    except Exception as e:
        logger.exception(f"/ingest failed | folder={req.folder} | error={e}")
        raise HTTPException(status_code=400, detail=str(e))

    dt = time.perf_counter() - t0
    logger.info(
        f"/ingest completed | folder={req.folder} | pdf_files={pdf_files} "
        f"| pages={loaded_pages} | chunks={chunks_created} | latency_s={dt:.3f}"
    )

    return IngestResponse(
        folder=req.folder,
        index_path=index_path,
        pdf_files=pdf_files,
        loaded_pages=loaded_pages,
        chunks_created=chunks_created,
    )


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    k = req.k or settings.default_k
    index_path = settings.default_index_path

    # Request-level override, else server default
    sanitize = req.sanitize if req.sanitize is not None else settings.enable_sanitization

    # --- Safety Wrapper ---
    decision = safety_wrapper(req.user_query, allow_sensitive=False)
    logger.info(f"/query called | meta={decision.meta}")

    if not decision.allowed:
        logger.warning(f"/query blocked | reason={decision.reason} | meta={decision.meta}")
        raise HTTPException(status_code=400, detail=decision.reason)

    
    t0 = time.perf_counter()
    logger.info("/query called | k=%s | sanitize=%s | query=%r", k, sanitize, req.user_query)

    try:
        answer, docs, sanitized_query  = answer_query(req.user_query, index_path=index_path, k=k, sanitize=sanitize,
            sanitize_context=settings.sanitize_context)
    except Exception as e:
        logger.exception(f"/query failed | error={e}")
        raise HTTPException(status_code=500, detail=str(e))

    dt = time.perf_counter() - t0
    logger.info(f"/query completed | k={k} | latency_s={dt:.3f}")

    # If sanitization is ON, sanitize sources content returned too
    sources = []
    for d in docs:
        content = d.page_content
        if sanitize:
            content = mask_private_data(content)
        sources.append(SourceChunk(content=content, metadata=d.metadata or {}))

    return QueryResponse(
        user_query=req.user_query,
        sanitized_query=sanitized_query,
        k=k,
        answer=answer,
        sources=sources,
    )