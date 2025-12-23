import qdrant_client
from qdrant_client.http import models
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from models.document import DocumentChunk

load_dotenv()

class VectorStoreService:
    def __init__(self):
        self.host = os.getenv("QDRANT_HOST")
        self.api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "ros2_humanoid_docs")

        if self.api_key:
            self.client = qdrant_client.QdrantClient(
                url=self.host,
                api_key=self.api_key
            )
        else:
            self.client = qdrant_client.QdrantClient(host=self.host)

        # Initialize collection if it doesn't exist
        self._initialize_collection()

    def _initialize_collection(self):
        """Initialize the Qdrant collection with appropriate vector configuration."""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
            )

    async def upsert_chunk(self, chunk: DocumentChunk):
        """Upsert a document chunk into the vector store."""
        try:
            points = [
                models.PointStruct(
                    id=chunk.id,
                    vector=chunk.embedding,
                    payload={
                        "document_id": chunk.document_id,
                        "content": chunk.content,
                        "chunk_index": chunk.chunk_index,
                        "metadata": chunk.metadata
                    }
                )
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return True
        except Exception as e:
            print(f"Error upserting chunk: {e}")
            return False

    async def upsert_chunks(self, chunks: List[DocumentChunk]):
        """Upsert multiple document chunks into the vector store."""
        try:
            points = []
            for chunk in chunks:
                point = models.PointStruct(
                    id=chunk.id,
                    vector=chunk.embedding,
                    payload={
                        "document_id": chunk.document_id,
                        "content": chunk.content,
                        "chunk_index": chunk.chunk_index,
                        "metadata": chunk.metadata
                    }
                )
                points.append(point)

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return True
        except Exception as e:
            print(f"Error upserting chunks: {e}")
            return False

    async def search(self, query_vector: List[float], limit: int = 5) -> List[Dict]:
        """Search for similar documents based on the query vector."""
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True
            )

            return [
                {
                    "id": result.id,
                    "document_id": result.payload["document_id"],
                    "content": result.payload["content"],
                    "chunk_index": result.payload["chunk_index"],
                    "metadata": result.payload["metadata"],
                    "similarity_score": result.score
                }
                for result in results
            ]
        except Exception as e:
            print(f"Error searching vector store: {e}")
            return []

    async def delete_document_chunks(self, document_id: str):
        """Delete all chunks associated with a document."""
        try:
            # Find all points with the document_id
            results = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="payload.document_id",
                            match=models.MatchValue(value=document_id)
                        )
                    ]
                ),
                limit=10000  # Assuming max chunks per document
            )

            point_ids = [point.id for point, _ in results]

            if point_ids:
                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=models.PointIdsList(
                        points=point_ids
                    )
                )

            return len(point_ids)
        except Exception as e:
            print(f"Error deleting document chunks: {e}")
            return 0

# Singleton instance
vector_store_service = VectorStoreService()