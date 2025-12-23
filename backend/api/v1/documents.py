from fastapi import APIRouter, HTTPException
from models.document import DocumentIngestRequest, DocumentIngestResponse
import os
import hashlib
from typing import List
import asyncio
from services.embedding import embedding_service
from services.vector_store import vector_store_service
from models.document import DocumentChunk
import uuid
import time

router = APIRouter()

def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # If this is the last chunk, make sure we include all remaining text
        if end >= len(text):
            chunks.append(text[start:])
            break

        # Find a good break point (try to break at sentence or paragraph boundary)
        chunk = text[start:end]

        # Add overlap if not the last chunk
        if end + overlap < len(text):
            chunk += text[end:end + overlap]

        chunks.append(chunk)
        start = end

    return chunks

@router.post("/documents/ingest", response_model=DocumentIngestResponse)
async def ingest_documents(request: DocumentIngestRequest):
    """Process Markdown files and store them in the vector database."""
    start_time = time.time()

    if not os.path.exists(request.source_directory):
        raise HTTPException(status_code=400, detail="Source directory does not exist")

    processed_files = 0
    total_chunks = 0

    # Process each Markdown file in the directory
    for filename in os.listdir(request.source_directory):
        if filename.endswith('.md'):
            file_path = os.path.join(request.source_directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Create document ID based on file path
            document_id = hashlib.md5(f"{request.source_directory}/{filename}".encode()).hexdigest()

            # Calculate checksum of content
            checksum = hashlib.md5(content.encode()).hexdigest()

            # Split content into chunks
            text_chunks = chunk_text(content, request.chunk_size, request.overlap)

            # Create embeddings for each chunk
            chunk_embeddings = await embedding_service.create_embeddings_batch(text_chunks)

            # Create DocumentChunk objects
            chunks_to_store = []
            for i, (chunk_text, chunk_embedding) in enumerate(zip(text_chunks, chunk_embeddings)):
                chunk = DocumentChunk(
                    id=str(uuid.uuid4()),
                    document_id=document_id,
                    content=chunk_text,
                    chunk_index=i,
                    embedding=chunk_embedding,
                    metadata={
                        "source_file": filename,
                        "directory": request.source_directory,
                        "chunk_size": request.chunk_size,
                        "overlap": request.overlap
                    }
                )
                chunks_to_store.append(chunk)

            # Store chunks in vector database
            success = await vector_store_service.upsert_chunks(chunks_to_store)

            if success:
                processed_files += 1
                total_chunks += len(chunks_to_store)

    processing_time = f"{time.time() - start_time:.2f}s"

    return DocumentIngestResponse(
        status="success",
        processed_files=processed_files,
        total_chunks=total_chunks,
        processing_time=processing_time
    )

@router.get("/documents/")
async def list_documents():
    """Retrieve a list of all indexed documents with metadata."""
    # This would typically query a database for document metadata
    # For now, we'll return a placeholder response
    return {
        "documents": []
    }

@router.get("/documents/{document_id}")
async def get_document(document_id: str):
    """Retrieve detailed information about a specific document."""
    # This would typically query a database for document details
    # For now, we'll return a placeholder response
    raise HTTPException(status_code=404, detail="Document not implemented yet")

@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Remove a document and its associated chunks from the vector database."""
    deleted_count = await vector_store_service.delete_document_chunks(document_id)

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "status": "success",
        "message": f"Document and {deleted_count} associated chunks deleted"
    }