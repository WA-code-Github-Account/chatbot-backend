from fastapi import APIRouter
from src.api.v1.endpoints import rag, documents, auth


# Create the main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(rag.router, prefix="/rag", tags=["rag"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])