# System Context for AI Agent

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) system that connects to PostgreSQL (Neon), Qdrant vector database, and Groq API to provide accurate, context-aware responses with source attribution.

## Core Technologies

- **Framework**: FastAPI
- **Database**: PostgreSQL (Neon) with SQLAlchemy and asyncpg
- **Vector Database**: Qdrant
- **LLM API**: Groq API
- **Authentication**: OAuth2 with JWT tokens
- **Concurrent Queries**: Up to 1000 concurrent queries
- **Languages**: English and Urdu support
- **Data Storage**: Documents up to 10MB

## Key Architecture Patterns

- Async/await for handling high concurrency
- RAG (Retrieval-Augmented Generation) pattern for accurate responses
- Document chunking: 500-1000 token chunks with 100-token overlap
- Source citation in format [Source: document_name, page/section]
- OAuth2 with role-based access control
- Microservice-like API structure with modular components

## Data Models

- Document: Stores original documents with metadata
- DocumentChunk: Represents segmented document parts for vector storage
- User: User accounts with role-based permissions
- UserQuery: Tracks queries and their responses with citations

## API Structure

- `/auth/` - Authentication endpoints using OAuth2
- `/documents/` - Document management endpoints
- `/rag/` - RAG query processing endpoints

## Critical Constraints

- Response time: <3 seconds for 90% of queries
- Accuracy: 95% accuracy for retrieved information
- Concurrency: Support 1000 concurrent queries
- Document size: Maximum 10MB per document
- Data retention: 1 year for user queries and logs
- Compliance: Never expose database credentials in responses

## Development Guidelines

- All responses must be grounded in provided document content (no hallucinations)
- Proper source attribution is mandatory in responses
- Error handling must be robust with alternative approaches when services fail
- Implement proper rate limiting and query logging
- Maintain 99% uptime during normal operating hours

## Important Endpoints

- POST `/auth/token` - Obtain OAuth2 token
- POST `/documents/upload` - Upload new document
- GET `/documents/` - List documents
- POST `/rag/query` - Submit query and receive RAG response

## Security Measures

- OAuth2 authentication with JWT tokens
- Sensitive information redaction
- Input validation and sanitization
- Rate limiting to prevent abuse
- Proper access controls on documents