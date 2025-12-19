from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import time
from uuid import UUID
import sys

from pathlib import Path
import os

# Get the project root directory (where the main project folder is)
# Going up from backend\src\api\v1\endpoints to project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent.parent.parent  # Go up 7 levels from endpoints to project root
BOOK_PATH = PROJECT_ROOT / "humanoid-robotics-book/docs-site/docs/physical-ai-humanoid-robotics"

print("PROJECT ROOT:", PROJECT_ROOT)
print("BOOK PATH:", BOOK_PATH)
print("BOOK EXISTS:", BOOK_PATH.exists())

def load_all_markdown_files(base_path: Path):
    documents = []

    for md_file in base_path.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            documents.append({
                "path": str(md_file),
                "content": content
            })
        except Exception as e:
            print(f"Failed to read {md_file}: {e}")

    return documents

# Only load documents if the book path exists
if BOOK_PATH.exists():
    DOCUMENTS = load_all_markdown_files(BOOK_PATH)
    print(f"TOTAL CHAPTER FILES LOADED: {len(DOCUMENTS)}")
else:
    print("BOOK PATH DOES NOT EXIST - USING EMPTY DOCUMENT SET")
    DOCUMENTS = []


router = APIRouter()


# Request/Response Models
class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    language: str = Field(default="en")

    @field_validator('language')
    def validate_language(cls, v):
        if v not in ['en', 'ur']:
            raise ValueError('Language must be either "en" for English or "ur" for Urdu')
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


class RAGQueryWithCitationRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    language: str = Field(default="en")
    include_metadata: bool = Field(default=True)

    @field_validator('language')
    def validate_language(cls, v):
        if v not in ['en', 'ur']:
            raise ValueError('Language must be either "en" for English or "ur" for Urdu')
        return v


# Simple test endpoint (No dependencies)
@router.post("/test", response_model=RAGQueryResponse)
async def test_query(request: RAGQueryRequest):
    """
    Simple test endpoint to verify backend is working
    Returns echo of your query
    """
    start_time = time.time()

    response_text = f"✅ Backend is working! You asked: '{request.query}'"

    if request.language == "ur":
        response_text = f"✅ بیک اینڈ کام کر رہا ہے! آپ نے پوچھا: '{request.query}'"

    query_time = (time.time() - start_time) * 1000

    return RAGQueryResponse(
        response=response_text,
        sources=[],
        query_time_ms=query_time,
        language=request.language
    )


def simple_search(query: str, documents: List[dict], top_k: int = 3):
    """
    Simple search function to find the most relevant documents for the query
    """
    query_lower = query.lower()
    results = []

    for doc in documents:
        content = doc["content"].lower()
        path = doc["path"]

        # Calculate a simple relevance score based on term frequency
        words = query_lower.split()
        score = 0
        for word in words:
            score += content.count(word)

        if score > 0:  # Only include documents that contain query terms
            results.append({
                "path": path,
                "content": doc["content"],
                "score": score
            })

    # Sort by score in descending order
    results.sort(key=lambda x: x["score"], reverse=True)

    # Return top_k results
    return results[:top_k]

# Main RAG endpoint (Simplified - no auth, no database logging)
@router.post("/query", response_model=RAGQueryResponse)
async def query_rag(request: RAGQueryRequest):
    """
    Main RAG query endpoint
    Submit a query and receive AI-enhanced response
    """
    start_time = time.time()

    try:
        # Check if documents were loaded
        if not DOCUMENTS:
            response_text = f"Book documents are not loaded. Please ensure the book path exists: {BOOK_PATH}"
            sources = []
        else:
            # Search for relevant documents in the book
            search_results = simple_search(request.query, DOCUMENTS, top_k=3)

            if search_results:
                # Format the context from the most relevant document
                context = search_results[0]["content"][:1000] + "..." if len(search_results[0]["content"]) > 1000 else search_results[0]["content"]
                response_text = f"Based on the book content:\n\n{context}\n\nRegarding your query: '{request.query}', I found relevant information in the book."

                # Create source citations
                sources = []
                for result in search_results:
                    sources.append(SourceCitation(
                        document_id=result["path"],
                        document_title=result["path"].split("/")[-1].replace(".md", ""),
                        text_preview=result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"],
                        similarity_score=result["score"],
                        source_type="document"
                    ))
            else:
                response_text = f"I couldn't find specific information about '{request.query}' in the book content. Please try rephrasing your question or check if the topic is covered in the book."
                sources = []

        if request.language == "ur" and DOCUMENTS:
            response_text = f"کتاب کے مواد کی بنیاد پر: \n\n{context}\n\nآپ کے سوال: '{request.query}' کے بارے میں، میں نے کتاب میں متعلقہ معلومات تلاش کیں۔" if 'search_results' in locals() and search_results else f"مجھے کتاب کے مواد میں '{request.query}' کے بارے میں مخصوص معلومات نہیں مل سکی۔ براہ کرم اپنا سوال دوبارہ کہنے کی کوشش کریں یا چیک کریں کہ کیا موضوع کتاب میں شامل ہے۔"

        query_time = (time.time() - start_time) * 1000

        return RAGQueryResponse(
            response=response_text,
            sources=sources,
            query_time_ms=query_time,
            language=request.language
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


# Query with citations endpoint
@router.post("/query-with-citation", response_model=RAGQueryResponse)
async def query_with_citation(request: RAGQueryWithCitationRequest):
    """
    Query with explicit source citations
    """
    start_time = time.time()

    try:
        response_text = (
            f"Query: '{request.query}' | "
            f"Citations feature ready. Upload documents to get cited responses."
        )

        if request.language == "ur":
            response_text = (
                f"سوال: '{request.query}' | "
                f"حوالہ جات کی سہولت تیار ہے۔ حوالہ جات کے ساتھ جوابات کے لیے دستاویزات اپ لوڈ کریں۔"
            )

        # Example citation structure
        example_citation = SourceCitation(
            document_id="example-doc-123",
            document_title="Example Document",
            page_number=1,
            section="Introduction",
            text_preview="This is an example citation...",
            similarity_score=0.95,
            source_type="document",
            chunk_id="chunk-001"
        )

        query_time = (time.time() - start_time) * 1000

        return RAGQueryResponse(
            response=response_text,
            sources=[example_citation] if DOCUMENTS else [],
            query_time_ms=query_time,
            language=request.language
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query with citation: {str(e)}"
        )


# Health check for RAG service
@router.get("/health")
async def rag_health():
    """Check if RAG service is operational"""
    return {
        "status": "healthy",
        "service": "RAG Endpoints",
        "endpoints_available": [
            "/test",
            "/query",
            "/query-with-citation"
        ]
    }