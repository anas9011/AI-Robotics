#!/usr/bin/env python3
"""
Document Ingestion Script for ROS 2 Humanoid Robotics RAG System

This script reads Markdown files from the documentation directory,
chunks the text, generates embeddings, and stores them in Qdrant.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.document import DocumentIngestRequest
from api.v1.documents import ingest_documents

async def main():
    """Main ingestion function."""
    print("Starting document ingestion process...")

    # Configuration
    request = DocumentIngestRequest(
        source_directory="docs/module-2",
        chunk_size=1000,
        overlap=200
    )

    # Check if source directory exists
    if not os.path.exists(request.source_directory):
        print(f"Error: Source directory '{request.source_directory}' does not exist.")
        print("Please make sure the docs/module-2 directory contains Markdown files.")
        return 1

    # Check if the directory has any Markdown files
    md_files = [f for f in os.listdir(request.source_directory) if f.endswith('.md')]
    if not md_files:
        print(f"Warning: No Markdown files found in '{request.source_directory}'")
        print("Please add .md files to the directory before running ingestion.")
        return 1

    print(f"Found {len(md_files)} Markdown files to process: {md_files}")

    # Run the ingestion
    try:
        result = await ingest_documents(request)
        print(f"Ingestion completed successfully!")
        print(f"Processed files: {result.processed_files}")
        print(f"Total chunks created: {result.total_chunks}")
        print(f"Processing time: {result.processing_time}")
        return 0
    except Exception as e:
        print(f"Error during ingestion: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)