from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    source_path: str
    module: str
    section: str

class DocumentCreate(DocumentBase):
    content: str

class Document(DocumentBase):
    id: str
    content: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    chunk_count: int
    checksum: str

    class Config:
        from_attributes = True

class DocumentChunk(BaseModel):
    id: str
    document_id: str
    content: str
    chunk_index: int
    embedding: Optional[List[float]] = None
    metadata: dict

    class Config:
        from_attributes = True

class DocumentIngestRequest(BaseModel):
    source_directory: str = "docs/module-2"
    chunk_size: int = 1000
    overlap: int = 200

class DocumentIngestResponse(BaseModel):
    status: str
    processed_files: int
    total_chunks: int
    processing_time: str