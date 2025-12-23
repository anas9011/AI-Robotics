# ROS 2 Humanoid Robotics RAG Backend

This FastAPI-based backend provides the RAG (Retrieval-Augmented Generation) functionality for the ROS 2 Humanoid Robotics Book documentation system.

## Architecture

The backend consists of:

- **API Layer**: FastAPI endpoints for document management and chat functionality
- **Service Layer**: Embedding, vector storage, and RAG services
- **Data Layer**: Integration with Qdrant vector database and document storage

## Setup

### Prerequisites

- Python 3.11+
- Access to OpenAI API
- Access to Qdrant Cloud (or local instance)
- Access to Neon PostgreSQL (or local instance)

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`:
   ```env
   NEON_DATABASE_URL=your_neon_database_url
   QDRANT_HOST=your_qdrant_host
   QDRANT_API_KEY=your_qdrant_api_key
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_COLLECTION_NAME=ros2_humanoid_docs
   ```

### Running the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Documents
- `POST /api/v1/documents/ingest` - Process and store documentation
- `GET /api/v1/documents/` - List available documents

### Chat
- `POST /api/v1/chat/query` - Submit a query and receive RAG-enhanced response
- `GET /api/v1/chat/session/{session_id}` - Retrieve conversation history
- `GET /api/v1/chat/health` - Health check endpoint

## Document Ingestion

To process documentation and store it in the vector database:

```bash
python scripts/ingest.py
```

This script will:
- Read Markdown files from the `docs/` directory
- Chunk text for optimal embedding
- Generate embeddings using OpenAI
- Upsert vectors into Qdrant Cloud

## Environment Configuration

The following environment variables are required:

- `OPENAI_API_KEY`: Your OpenAI API key for embeddings and chat generation
- `QDRANT_HOST`: Host URL for your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant (if using cloud version)
- `QDRANT_COLLECTION_NAME`: Name of the collection to store document vectors
- `NEON_DATABASE_URL`: Connection string for PostgreSQL database (future use)

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── models/                 # Pydantic data models
│   ├── document.py         # Document data models
│   └── query.py            # Query request/response models
├── services/               # Business logic services
│   ├── embedding.py        # Embedding generation service
│   ├── vector_store.py     # Qdrant integration
│   └── rag.py             # RAG (Retrieval-Augmented Generation) service
├── api/                   # API route definitions
│   └── v1/                # Version 1 API endpoints
│       ├── documents.py   # Document management endpoints
│       └── chat.py        # Chat interface endpoints
└── scripts/               # Utility scripts
    └── ingest.py          # Document ingestion script
```

## Testing

To test the API:

```bash
# Health check
curl http://localhost:8000/health

# Test document ingestion
curl -X POST http://localhost:8000/api/v1/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{"source_directory": "docs/module-2", "chunk_size": 1000, "overlap": 200}'

# Test chat query
curl -X POST http://localhost:8000/api/v1/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Gazebo physics?", "context": "", "session_id": "test-session"}'
```