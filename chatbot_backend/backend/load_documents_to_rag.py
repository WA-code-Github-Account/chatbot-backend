#!/usr/bin/env python3
"""
Script to load book documents into the RAG system
This script will read all documents from the data/documents directory,
process them into chunks, generate embeddings, and store them in the vector database.
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
from uuid import uuid4

# Add the backend directory to the path so we can import modules
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from config.database import DATABASE_URL
from src.services.document_service import DocumentService
from src.services.vector_service import VectorService
from src.services.llm_service import LLMService
from src.utils.document_processor import DocumentProcessor
from src.models.document import Document
from src.models.document_chunk import DocumentChunk
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def load_documents_to_rag():
    """Load all book documents into the RAG system"""
    logger.info("Starting document loading process...")
    
    # Initialize database connection
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Initialize services
    vector_service = VectorService()
    llm_service = LLMService()
    document_processor = DocumentProcessor()
    
    # Get all markdown files from the data/documents directory
    documents_path = backend_path / "data" / "documents"
    
    if not documents_path.exists():
        logger.error(f"Documents directory not found: {documents_path}")
        return
    
    # Find all .md files recursively
    md_files = list(documents_path.rglob("*.md"))
    logger.info(f"Found {len(md_files)} markdown files to process")
    
    async with async_session() as session:
        doc_service = DocumentService(session)
        
        for md_file in md_files:
            logger.info(f"Processing: {md_file}")
            
            try:
                # Read the document content
                content = md_file.read_text(encoding='utf-8')
                
                # Create a document record
                document = await doc_service.create_document(
                    title=md_file.stem,  # Use filename without extension as title
                    content=content,
                    source_type="text/markdown",
                    user_id=uuid4(),  # Using a random UUID for the system user
                    metadata=f"Book content from {md_file.relative_to(documents_path)}",
                    page_count=len(content.splitlines())  # Approximate page count
                )
                
                logger.info(f"Created document: {document.title} (ID: {document.id})")
                
                # Process the document content into chunks
                processed_result = document_processor.process_document_content(content, "text/markdown")
                chunks = processed_result["chunks"]
                
                logger.info(f"Split document into {len(chunks)} chunks")
                
                # Process each chunk
                for i, chunk_data in enumerate(chunks):
                    # Generate embedding for the chunk
                    embedding = await llm_service.generate_embedding(chunk_data["content"])
                    
                    # Store the embedding in the vector database
                    chunk_id = str(uuid4())
                    metadata = {
                        "content": chunk_data["content"],
                        "document_id": str(document.id),
                        "document_title": document.title,
                        "chunk_order": chunk_data["chunk_order"],
                        "source_file": str(md_file.relative_to(documents_path))
                    }
                    
                    success = await vector_service.store_embedding(
                        chunk_id=chunk_id,
                        embedding=embedding,
                        metadata=metadata
                    )
                    
                    if success:
                        logger.info(f"Stored chunk {i+1}/{len(chunks)} for document {document.title}")
                    else:
                        logger.error(f"Failed to store chunk {i+1} for document {document.title}")
                
                logger.info(f"Completed processing: {document.title}")
                
            except Exception as e:
                logger.error(f"Error processing file {md_file}: {str(e)}")
                continue
    
    logger.info("Document loading process completed!")


if __name__ == "__main__":
    asyncio.run(load_documents_to_rag())