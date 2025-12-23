from fastapi import APIRouter, HTTPException
from models.query import QueryRequest, QueryResponse
from services.rag import rag_service
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/chat/query", response_model=QueryResponse)
async def query_chat(request: QueryRequest):
    """Submit a user query and return a RAG-enhanced response."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question must not be empty")

    # Process the query using RAG service
    response = await rag_service.process_query(request)

    return response

@router.get("/chat/session/{session_id}")
async def get_conversation_history(session_id: str):
    """Retrieve the conversation history for a specific session."""
    # This would typically query a database for conversation history
    # For now, we'll return a placeholder response
    return {
        "session_id": session_id,
        "history": []
    }

@router.delete("/chat/session/{session_id}")
async def clear_session(session_id: str):
    """Clear the conversation history for a specific session."""
    # This would typically delete session data from a database
    # For now, we'll return a placeholder response
    return {
        "status": "success",
        "message": "Session history cleared"
    }

@router.get("/chat/health")
async def chat_health():
    """Check the health status of the chat service and its dependencies."""
    # Check if required services are available
    dependencies = {
        "vector_store": "connected",  # This would check actual connection
        "llm_service": "available",  # This would check actual connection
        "database": "connected"  # This would check actual connection
    }

    return {
        "status": "healthy",
        "dependencies": dependencies,
        "timestamp": datetime.now()
    }