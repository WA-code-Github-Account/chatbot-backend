from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from src.services.document_service import DocumentService
from src.middleware.auth import get_current_user
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
import logging


router = APIRouter()
logger = logging.getLogger(__name__)


# Request models
class DocumentCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    source_type: str  # e.g., 'PDF', 'text', 'web page', 'docx'


class DocumentUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Response models
class DocumentResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    source_type: str
    upload_date: str
    user_id: UUID
    page_count: Optional[int]
    chunk_count: Optional[int]


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = None,
    description: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a new document
    """
    try:
        # Validate file size (max 10MB as per spec)
        # Note: This is a simplified check - in a real implementation, 
        # you'd need to check the actual size before storing in memory
        if file.size and file.size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds 10MB limit"
            )
        
        # Validate file type
        allowed_types = ["application/pdf", "text/plain", "text/html", "application/msword", 
                         "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file.content_type} not supported. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8') if isinstance(content, bytes) else content
        
        # Initialize document service
        doc_service = DocumentService(db)
        
        # Create document
        document = await doc_service.create_document_with_metadata(
            title=title or file.filename,
            content=content_str,
            source_type=file.content_type,
            user_id=UUID(current_user["user_id"]),
            metadata={"filename": file.filename, "size": file.size},
            page_count=0,  # This would be calculated in a real implementation
        )
        
        # For now, return basic document info
        # In a real implementation, you'd also process and chunk the document
        return DocumentResponse(
            id=document.id,
            title=document.title,
            description=description,
            source_type=document.source_type,
            upload_date=document.upload_date.isoformat() if document.upload_date else "",
            user_id=document.user_id,
            page_count=document.page_count,
            chunk_count=0  # Would be populated after processing
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error uploading document"
        )


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List documents for the current user
    """
    try:
        # Initialize document service
        doc_service = DocumentService(db)
        
        # Get user's documents
        documents = await doc_service.get_documents_by_user(
            user_id=UUID(current_user["user_id"]),
            skip=skip,
            limit=limit
        )
        
        # Convert to response format
        response_docs = []
        for doc in documents:
            response_docs.append(DocumentResponse(
                id=doc.id,
                title=doc.title,
                description=None,  # Would come from metadata in a complete implementation
                source_type=doc.source_type,
                upload_date=doc.upload_date.isoformat() if doc.upload_date else "",
                user_id=doc.user_id,
                page_count=doc.page_count,
                chunk_count=0  # Would be calculated from associated chunks
            ))
        
        return response_docs
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error listing documents"
        )


@router.delete("/{document_id}")
async def delete_document(
    document_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a specific document
    """
    try:
        # Initialize document service
        doc_service = DocumentService(db)
        
        # Verify document belongs to user (in a complete implementation)
        # For now, just attempt deletion
        success = await doc_service.delete_document(document_id)
        
        if success:
            return {"message": f"Document {document_id} deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document {document_id} not found"
            )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error deleting document {document_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting document"
        )