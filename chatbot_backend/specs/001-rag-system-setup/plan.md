# Implementation Plan: RAG System Setup

**Branch**: `001-rag-system-setup` | **Date**: 2025-12-16 | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a Retrieval-Augmented Generation (RAG) system that connects to PostgreSQL (Neon), Qdrant vector database, and Groq API to provide accurate, context-aware responses with source attribution. The system will support multi-language queries in English and Urdu while maintaining 95% accuracy, <3s response times, and 1000 concurrent query support.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, Qdrant client, SQLAlchemy, Groq API client, Pydantic, asyncpg
**Storage**: PostgreSQL (Neon) for document metadata and user queries, Qdrant for vector storage
**Testing**: pytest with integration and unit tests
**Target Platform**: Linux server (cloud deployment)
**Project Type**: Web backend with API endpoints
**Performance Goals**: Handle up to 1000 concurrent queries with <3s response time for 90% of requests
**Constraints**: <100MB memory usage, operate within free tier limits of Neon, Qdrant, and Groq API
**Scale/Scope**: Support up to 500-page books with 10MB max document size, 95% information accuracy

## Constitution Check

The implementation must:
- Answer ONLY from provided document content (no hallucinations)
- Maintain <3 second response time under load
- Support text selection queries with page citations
- Operate within free tier limits of services
- Maintain fidelity of document content during processing
- Handle books up to 500 pages with efficient vector storage

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── document.py          # Document and chunk models
│   │   ├── user_query.py        # User query models
│   │   └── response.py          # Response models
│   ├── services/
│   │   ├── rag_service.py       # Main RAG service
│   │   ├── document_service.py  # Document ingestion and management
│   │   ├── vector_service.py    # Vector database operations
│   │   └── llm_service.py       # LLM interaction
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── rag.py       # Main RAG endpoints
│   │   │   │   ├── documents.py # Document management
│   │   │   │   └── auth.py      # Authentication endpoints
│   │   │   └── router.py        # API router
│   │   └── dependencies.py      # Dependency injection
│   └── main.py                  # Application entry point
├── config/
│   ├── settings.py              # Configuration settings
│   └── database.py              # Database configuration
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── requirements.txt
```

**Structure Decision**: Web application structure chosen as the RAG system will provide API endpoints for querying documents and managing the knowledge base.

## Phase 0: Research

### Research Tasks and Findings

1. **Authentication Implementation**:
   - Decision: Implement OAuth2 with JWT tokens
   - Rationale: Standard implementation that provides role-based access control as specified
   - Alternatives considered: Basic auth, API keys; JWT chosen for better RBAC support

2. **Async vs Sync Processing**:
   - Decision: Use async/await pattern throughout the application
   - Rationale: Better performance for I/O-bound operations like database queries and API calls
   - Alternatives considered: Synchronous processing; async chosen for better concurrency

3. **Qdrant Integration**:
   - Decision: Use Qdrant's Python client with point IDs matching document chunk IDs
   - Rationale: Allows efficient retrieval of document chunks with metadata
   - Alternatives considered: Other vector databases; Qdrant chosen as per spec

4. **Multi-language Support**:
   - Decision: Use language detection followed by appropriate processing pipeline
   - Rationale: Enables bilingual support as specified while maintaining accuracy
   - Alternatives considered: Separate models for each language; unified approach chosen

5. **Document Chunking Strategy**:
   - Decision: 500-1000 token chunks with 100-token overlap as per constitution
   - Rationale: Balances retrieval accuracy with cost efficiency
   - Alternatives considered: Fixed-size chunks; token-based chunks chosen for better semantic boundaries

## Phase 1: Design & Contracts

### Data Model

The data model includes:

1. **Document Model**:
   - id: UUID
   - title: String
   - content: Text
   - metadata: JSON
   - upload_date: DateTime
   - source_type: String (PDF, text, web page)

2. **DocumentChunk Model**:
   - id: UUID
   - document_id: UUID (foreign key)
   - content: Text
   - chunk_order: Integer
   - metadata: JSON
   - embedding_id: String (ID in Qdrant)

3. **UserQuery Model**:
   - id: UUID
   - query_text: Text
   - user_id: UUID
   - timestamp: DateTime
   - response: Text
   - source_citations: JSON

4. **User Model**:
   - id: UUID
   - username: String
   - email: String
   - oauth2_token: String
   - role: String (user, admin)

### API Contracts

The API will follow REST principles with the following endpoints:

1. **Authentication**:
   - `POST /auth/token` - OAuth2 token generation
   - `GET /auth/profile` - Get user profile (with auth)

2. **Document Management**:
   - `POST /documents/upload` - Upload new document (with auth)
   - `GET /documents/` - List documents (with auth)
   - `DELETE /documents/{id}` - Delete document (admin only)

3. **RAG Query**:
   - `POST /rag/query` - Submit query and receive RAG-enhanced response
   - `POST /rag/query-with-citation` - Query with explicit source citations

### Quickstart Guide

```bash
# 1. Clone the repository
git clone <repository-url>
cd <repository-name>

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your database credentials and API keys

# 5. Run database migrations
python -m alembic upgrade head

# 6. Start the application
uvicorn src.main:app --reload

# 7. Test the API
curl -X POST http://localhost:8000/api/v1/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Your question here", "language": "en"}'
```

### Agent Context Update

The following technologies and patterns will be added to the agent context:
- FastAPI for web framework
- Qdrant for vector storage
- PostgreSQL with asyncpg for relational data
- OAuth2 with JWT for authentication
- Async/await for concurrency
- RAG (Retrieval-Augmented Generation) pattern

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple external services | RAG pipeline requires vector DB, relational DB, and LLM API | Single-service solutions insufficient for RAG architecture |