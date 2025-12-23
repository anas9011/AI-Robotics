# Data Model: Digital Twin Content and RAG Chatbot

## Overview
This document defines the data models for the Module 2 content and RAG chatbot system, including document storage, vector embeddings, and query interfaces.

## Core Entities

### Document
Represents a documentation page or section that will be indexed for RAG queries.

**Fields**:
- `id` (string): Unique identifier for the document
- `title` (string): Title of the document section
- `content` (string): The text content of the document
- `source_path` (string): File path where the content originates
- `module` (string): Module identifier (e.g., "module-2")
- `section` (string): Specific section within the module
- `created_at` (datetime): Timestamp when the document was indexed
- `updated_at` (datetime): Timestamp when the document was last updated
- `checksum` (string): Hash to detect content changes

### DocumentChunk
Represents a processed chunk of a document that gets embedded and stored in the vector database.

**Fields**:
- `id` (string): Unique identifier for the chunk
- `document_id` (string): Reference to the parent document
- `content` (string): The chunked text content
- `chunk_index` (integer): Position of the chunk within the document
- `embedding` (vector): Vector representation of the content
- `metadata` (JSON): Additional metadata including source location

### Query
Represents a user query to the RAG system.

**Fields**:
- `id` (string): Unique identifier for the query
- `question` (string): The user's question
- `user_id` (string): Identifier for the user (optional for anonymous)
- `session_id` (string): Identifier for the conversation session
- `timestamp` (datetime): When the query was submitted
- `context` (string): Selected text context from the document (if applicable)

### QueryResponse
Represents the response from the RAG system to a user query.

**Fields**:
- `id` (string): Unique identifier for the response
- `query_id` (string): Reference to the original query
- `answer` (string): The AI-generated answer
- `context_used` (array): List of document chunks used to generate the answer
- `confidence_score` (float): Confidence level of the response (0.0-1.0)
- `timestamp` (datetime): When the response was generated
- `sources` (array): List of source documents referenced

## Relationships

### Document to DocumentChunk
- One-to-Many: A single document can be split into multiple chunks
- Foreign Key: `document_id` in DocumentChunk references `id` in Document

### Query to QueryResponse
- One-to-One: Each query generates one response
- Foreign Key: `query_id` in QueryResponse references `id` in Query

## Validation Rules

### Document
- `title` must be 1-200 characters
- `content` must not be empty
- `source_path` must be a valid path format
- `module` must match existing module identifiers

### DocumentChunk
- `content` must be between 100-2000 characters (for optimal embedding)
- `chunk_index` must be non-negative
- `embedding` must be a valid vector format

### Query
- `question` must be 1-1000 characters
- `session_id` must be provided if `user_id` is not provided

## State Transitions

### Document States
- `created`: Document has been parsed from source
- `chunked`: Document has been split into processable chunks
- `embedded`: All chunks have been converted to vector embeddings
- `indexed`: Document is ready for RAG queries

### Query States
- `submitted`: Query has been received by the system
- `processing`: System is retrieving relevant context
- `answering`: AI is generating the response
- `completed`: Response has been returned to the user