import asyncio
from typing import List, Dict
from models.query import QueryRequest, QueryResponse, DocumentContext, SourceDocument
from models.document import DocumentChunk
from services.embedding import embedding_service
from services.vector_store import vector_store_service
import uuid
from datetime import datetime

class RAGService:
    def __init__(self):
        pass

    async def process_query(self, query_request: QueryRequest) -> QueryResponse:
        """Process a user query using RAG (Retrieval-Augmented Generation)."""
        # Generate embedding for the user's question
        query_embedding = await embedding_service.create_embedding(query_request.question)

        # Search for relevant document chunks
        search_results = await vector_store_service.search(query_embedding, limit=5)

        # Prepare context from search results
        context_texts = []
        context_used = []
        sources = set()

        for result in search_results:
            context_texts.append(result["content"])
            context_used.append(
                DocumentContext(
                    document_id=result["document_id"],
                    chunk_id=result["id"],
                    content=result["content"],
                    similarity_score=result["similarity_score"]
                )
            )
            # For now, we'll use a simple source identifier based on document ID
            sources.add(result["document_id"])

        # Combine the context with the original question and optional user context
        full_context = "\n\n".join(context_texts)
        if query_request.context:
            full_context = f"User selected context: {query_request.context}\n\nRelevant documentation:\n{full_context}"

        # Generate the answer using OpenAI
        answer = await self.generate_answer(query_request.question, full_context)

        # Calculate confidence score based on similarity scores
        confidence_score = self.calculate_confidence(search_results)

        # Create response
        response = QueryResponse(
            id=str(uuid.uuid4()),
            query_id=str(uuid.uuid4()),  # In a real system, this would link to the actual query
            answer=answer,
            context_used=context_used,
            confidence_score=confidence_score,
            sources=[SourceDocument(id=src, title=f"Document {src}", source_path=f"docs/{src}") for src in sources],
            timestamp=datetime.now()
        )

        return response

    async def generate_answer(self, question: str, context: str) -> str:
        """Generate an answer using OpenAI based on the question and context."""
        import openai
        import os
        from dotenv import load_dotenv

        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        try:
            prompt = f"""Answer the following question based on the provided context from the ROS 2 Humanoid Robotics documentation.

Context:
{context}

Question: {question}

Answer: """

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert assistant for the ROS 2 Humanoid Robotics Book. Answer questions based on the provided documentation context. If the answer is not in the context, state that you don't have enough information from the documentation to answer the question."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "I encountered an error while generating the answer. Please try again later."

    def calculate_confidence(self, search_results: List[Dict]) -> float:
        """Calculate a confidence score based on similarity scores."""
        if not search_results:
            return 0.0

        # Average the top similarity scores
        similarities = [result["similarity_score"] for result in search_results]
        avg_similarity = sum(similarities) / len(similarities)

        # Normalize to 0-1 range (Qdrant similarity scores are typically 0-1)
        return min(1.0, avg_similarity)

# Singleton instance
rag_service = RAGService()