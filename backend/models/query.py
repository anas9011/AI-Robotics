from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QueryBase(BaseModel):
    question: str
    session_id: str
    user_id: Optional[str] = None

class QueryCreate(QueryBase):
    context: Optional[str] = ""

class Query(QueryBase):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True

class DocumentContext(BaseModel):
    document_id: str
    chunk_id: str
    content: str
    similarity_score: float

class SourceDocument(BaseModel):
    id: str
    title: str
    source_path: str

class QueryResponse(BaseModel):
    id: str
    query_id: str
    answer: str
    context_used: List[DocumentContext]
    confidence_score: float
    sources: List[SourceDocument]
    timestamp: datetime

    class Config:
        from_attributes = True

class QueryRequest(BaseModel):
    question: str
    context: Optional[str] = ""
    session_id: str
    user_id: Optional[str] = None

class QueryResponsePayload(BaseModel):
    id: str
    query_id: str
    answer: str
    context_used: List[dict]
    confidence_score: float
    sources: List[dict]
    timestamp: datetime