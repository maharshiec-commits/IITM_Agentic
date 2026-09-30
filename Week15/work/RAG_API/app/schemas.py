from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class IngestRequest(BaseModel):
    folder: str = Field(..., description="Folder path containing documents (PDFs).")
    index_path: Optional[str] = Field(None, description="Where to save the FAISS index.")

class IngestResponse(BaseModel):
    folder: str
    index_path: str
    pdf_files: int
    loaded_pages: int
    chunks_created: int

# class QueryRequest(BaseModel):
#     user_query: str = Field(..., min_length=1)
#     k: Optional[int] = Field(None, ge=1, le=20)

class QueryRequest(BaseModel):
    user_query: str = Field(..., min_length=1)  
    k: Optional[int] = Field(None, ge=1, le=20)
    sanitize: Optional[bool] = Field(
        None, description="Override sanitization for this request. If null, uses server default."
    )


class SourceChunk(BaseModel):
    content: str
    metadata: Dict[str, Any]

class QueryResponse(BaseModel):
    user_query: str
    sanitized_query: str
    k: int
    answer: str
    sources: List[SourceChunk]