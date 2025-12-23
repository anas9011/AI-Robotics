import openai
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class EmbeddingService:
    def __init__(self):
        self.model = "text-embedding-ada-002"

    async def create_embedding(self, text: str) -> List[float]:
        """Create an embedding for the given text using OpenAI API."""
        try:
            response = openai.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error creating embedding: {e}")
            raise e

    async def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for a batch of texts."""
        try:
            response = openai.embeddings.create(
                input=texts,
                model=self.model
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"Error creating batch embeddings: {e}")
            raise e

# Singleton instance
embedding_service = EmbeddingService()