from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from src.services.rag_service import RAGService
from uuid import UUID
import time
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# -----------------------------
# Request/Response Models
# -----------------------------
class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    language: str = Field(default="en")

    @field_validator('language')
    def validate_language(cls, v):
        if v not in ['en', 'ur', 'detect']:
            raise ValueError('Language must be "en", "ur", or "detect"')
        return v


class SourceCitation(BaseModel):
    document_id: Optional[str] = None
    document_title: Optional[str] = None
    page_number: Optional[int] = None
    section: Optional[str] = None
    text_preview: Optional[str] = None
    similarity_score: Optional[float] = None
    source_url: Optional[str] = None
    source_type: Optional[str] = None
    chunk_id: Optional[str] = None


class RAGQueryResponse(BaseModel):
    response: str
    sources: List[SourceCitation] = []
    query_time_ms: float = 0
    language: str = "en"


# -----------------------------
# Test Endpoint
# -----------------------------
@router.post("/test", response_model=RAGQueryResponse)
async def test_query(request: RAGQueryRequest):
    """Simple test endpoint"""
    start_time = time.time()
    response_text = f"✅ Backend is working! You asked: '{request.query}'"
    if request.language == "ur":
        response_text = f"✅ بیک اینڈ کام کر رہا ہے! آپ نے پوچھا: '{request.query}'"
    query_time = (time.time() - start_time) * 1000
    return RAGQueryResponse(response=response_text, sources=[], query_time_ms=query_time, language=request.language)


# -----------------------------
# Main RAG Endpoint
# -----------------------------
@router.post("/query", response_model=RAGQueryResponse)
async def query_rag(request: RAGQueryRequest, db: AsyncSession = Depends(get_db)):
    """Full RAG query"""
    start_time = time.time()
    try:
        system_user_id = UUID('12345678-1234-5678-1234-123456789abc')
        rag_service = RAGService(db)

        result = await rag_service.process_query(
            query_text=request.query,
            user_id=system_user_id,
            language=request.language
        )

        query_time = (time.time() - start_time) * 1000

        sources = []
        for source in result.get('sources', []):
            sources.append(SourceCitation(
                document_id=source.get('document_id'),
                document_title=source.get('document_title', 'Unknown Document'),
                text_preview=source.get('content_preview', '')[:200],
                similarity_score=source.get('score', 0),
                source_type=source.get('source_type', 'document')
            ))

        return RAGQueryResponse(
            response=result['response'],
            sources=sources,
            query_time_ms=result.get('query_time_ms', query_time),
            language=result.get('language', request.language)
        )
    except Exception as e:
        logger.error(f"Error processing RAG query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


# -----------------------------
# Query With Citation
# -----------------------------
@router.post("/query-with-citation", response_model=RAGQueryResponse)
async def query_with_citation(request: RAGQueryRequest, db: AsyncSession = Depends(get_db)):
    """Query returning sources explicitly"""
    return await query_rag(request, db)


# -----------------------------
# Health Check
# -----------------------------
@router.get("/health")
async def rag_health():
    return {
        "status": "healthy",
        "service": "RAG Endpoints",
        "endpoints_available": ["/test", "/query", "/query-with-citation"]
    }
