<!--
Sync Impact Report:
- Version change: N/A (initial version) → 1.0.0
- Modified principles: N/A (new project with initial constitution)
- Added sections: All principles and sections as specified for the RAG Chatbot project
- Removed sections: N/A
- Templates requiring updates: N/A (initial creation, templates are generic)
- Follow-up TODOs: None
-->
# Integrated RAG Chatbot for Published Book Constitution

## Core Principles

### Accuracy
Answer ONLY from book content, no hallucinations. All responses must be grounded in the provided book content.

### Performance
<3 second response time, handle 10+ concurrent users. System must maintain low latency even under load.

### User Experience
Support text selection queries, provide page citations. The interface must be intuitive and provide clear attribution to book sources.

### Cost Efficiency
Operate entirely within free tier limits. System must be designed to minimize costs while maximizing functionality.

### Data Integrity
Maintain fidelity of book content during processing. Preserve page numbers, formatting, and meaning during chunking and retrieval.

### Scalability
Designed to handle books up to 500 pages with limited storage constraints. System must efficiently manage vector storage limits.

## Technical Standards

- Data ingestion: 500-1000 token chunks with 100-token overlap, metadata preserved
- Vector storage: Qdrant with cosine similarity, sentence-transformers embeddings
- RAG pipeline: Query → Embed → Search (top-k=5) → Context → Grok API → Response
- Prompt template: System prompt enforces 'answer only from context' rule
- API integration: Grok API with streaming, temperature=0.3, max_tokens=500
- Frontend: Lightweight JS widget (<50KB), text selection support

## Constraints

- Qdrant free tier: 1GB storage (~250K chunks)
- Neon Postgres: 512MB storage, 100 hours compute/month
- Grok API: 60 requests/minute (estimated)
- Book size: Max 500 pages
- Conversation length: Max 10 turns per session

## Governance

- All implementations must comply with accuracy principle - no hallucinations allowed
- Performance benchmarks must be met before production deployment
- System must operate within defined cost constraints
- Rate limits and error handling must be implemented to ensure reliability

**Version**: 1.0.0 | **Ratified**: 2025-01-15 | **Last Amended**: 2025-01-15
