# Quickstart Guide: Digital Twin Content and RAG Chatbot

## Overview
This guide provides step-by-step instructions to set up the Module 2 content and RAG chatbot infrastructure for the ROS 2 Humanoid Robotics Book.

## Prerequisites
- Python 3.11+
- Node.js 18+
- Git
- Access to OpenAI API
- Access to Qdrant Cloud (or local instance)
- Access to Neon PostgreSQL (or local instance)

## Setup Steps

### 1. Clone and Initialize the Repository
```bash
git clone <repository-url>
cd <repository-name>
npm install
```

### 2. Set Up Backend Environment
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root with the following variables:

```env
NEON_DATABASE_URL=your_neon_database_url
QDRANT_HOST=your_qdrant_host
QDRANT_API_KEY=your_qdrant_api_key
OPENAI_API_KEY=your_openai_api_key
QDRANT_COLLECTION_NAME=ros2_humanoid_docs
```

### 4. Create Module 2 Content Directory
```bash
mkdir -p docs/module-2
```

### 5. Generate Module 2 Content
Create the following files in the `docs/module-2/` directory:

- `intro.md` - Overview of the digital twin concept
- `2.1-gazebo-physics.md` - Focus on URDF and ODE engine
- `2.2-unity-rendering.md` - High-fidelity HRI simulation
- `2.3-sensor-simulation.md` - LiDAR, Depth Cameras, and IMU data streams

### 6. Update Docusaurus Sidebar
Add the Module 2 entries to `sidebars.js`:

```javascript
{
  type: 'category',
  label: 'Module 2: The Digital Twin',
  items: [
    'module-2/intro',
    'module-2/2.1-gazebo-physics',
    'module-2/2.2-unity-rendering',
    'module-2/2.3-sensor-simulation'
  ],
}
```

### 7. Set Up the RAG Ingestion Process
Run the ingestion script to process documentation and store embeddings:

```bash
cd backend
python scripts/ingest.py
```

This script will:
- Read Markdown files from the `docs/` directory
- Chunk text for optimal embedding
- Generate embeddings using OpenAI
- Upsert vectors into Qdrant Cloud

### 8. Start the FastAPI Backend
```bash
cd backend
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### 9. Create the Chatbot Component
Create the React component in `src/components/Chatbot/`:

```
src/components/Chatbot/
├── Chatbot.jsx
├── ChatInterface.jsx
└── SelectionHandler.jsx
```

### 10. Integrate Chatbot with Frontend
Add the chatbot component to your Docusaurus pages:

```jsx
import Chatbot from '@site/src/components/Chatbot/Chatbot';

function MyPage() {
  return (
    <div>
      <main>Documentation content here</main>
      <Chatbot />
    </div>
  );
}
```

### 11. Run the Docusaurus Frontend
```bash
npm run start
```

The documentation site will be available at `http://localhost:3000`.

## Verification Steps

### 1. Test Document Ingestion
- Verify that documents are properly chunked and stored in Qdrant
- Check that embeddings are generated without errors

### 2. Test RAG Queries
- Submit a test query to the backend API
- Verify that relevant context is retrieved from the vector database

### 3. Test Frontend Integration
- Navigate to the documentation site
- Verify that the chatbot component is visible and functional
- Test selection-based querying by highlighting text and asking questions

## API Endpoints

### Document Management
- `POST /api/v1/documents/ingest` - Process and store documentation
- `GET /api/v1/documents/` - List available documents

### Chat Interface
- `POST /api/v1/chat/query` - Submit a query and receive RAG-enhanced response
- `GET /api/v1/chat/session/{session_id}` - Retrieve conversation history

## Troubleshooting

### Common Issues
1. **Environment variables not loaded**: Ensure `.env` file is properly configured and located in the correct directory
2. **Qdrant connection errors**: Verify QDRANT_HOST and QDRANT_API_KEY are correct
3. **OpenAI API errors**: Check that OPENAI_API_KEY is valid and has sufficient quota
4. **Document ingestion fails**: Verify that docs/ directory contains valid Markdown files

### Testing the Setup
```bash
# Test API connectivity
curl http://localhost:8000/health

# Test vector search
curl -X POST http://localhost:8000/api/v1/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Gazebo physics?", "context": ""}'
```