from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from src.models.document import Document
from src.models.document_chunk import DocumentChunk
from src.models.user import User
from src.utils.document_processor import DocumentProcessor
from typing import List, Optional, Dict
from uuid import UUID
import uuid
import logging


logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_document(
        self,
        title: str,
        content: str,
        source_type: str,
        user_id: UUID,
        metadata: Optional[str] = None,
        page_count: Optional[int] = None,
        source_url: Optional[str] = None,
        chunk_count: Optional[int] = None
    ) -> Document:
        """Create a new document record"""
        try:
            # Check if user exists
            user_exists = await self.db_session.get(User, user_id)
            if not user_exists:
                raise ValueError(f"User with ID {user_id} does not exist")

            # Create document instance with additional source tracking metadata
            document = Document(
                id=uuid.uuid4(),
                title=title,
                content=content,
                doc_metadata=metadata,
                source_type=source_type,
                user_id=user_id,
                page_count=page_count
            )

            # Add to session and commit
            self.db_session.add(document)
            await self.db_session.commit()
            await self.db_session.refresh(document)

            logger.info(f"Document created with ID: {document.id}")
            return document
        except Exception as e:
            logger.error(f"Error creating document: {str(e)}")
            await self.db_session.rollback()
            raise

    async def create_document_with_metadata(
        self,
        title: str,
        content: str,
        source_type: str,
        user_id: UUID,
        metadata: Optional[dict] = None,
        page_count: Optional[int] = None,
        source_url: Optional[str] = None,
        chunk_count: Optional[int] = None
    ) -> Document:
        """Create a new document with enhanced metadata tracking"""
        try:
            # Check if user exists
            user_exists = await self.db_session.get(User, user_id)
            if not user_exists:
                raise ValueError(f"User with ID {user_id} does not exist")

            # Convert metadata dict to JSON string if provided
            metadata_str = None
            if metadata:
                import json
                metadata_str = json.dumps(metadata)

            # Create document instance with additional source tracking metadata
            document = Document(
                id=uuid.uuid4(),
                title=title,
                content=content,
                doc_metadata=metadata_str,
                source_type=source_type,
                user_id=user_id,
                page_count=page_count
            )

            # Add to session and commit
            self.db_session.add(document)
            await self.db_session.commit()
            await self.db_session.refresh(document)

            logger.info(f"Document created with ID: {document.id} and metadata tracking")
            return document
        except Exception as e:
            logger.error(f"Error creating document with metadata: {str(e)}")
            await self.db_session.rollback()
            raise

    async def get_document_by_id(self, document_id: UUID) -> Optional[Document]:
        """Get a document by its ID"""
        try:
            stmt = select(Document).where(Document.id == document_id)
            result = await self.db_session.execute(stmt)
            document = result.scalar_one_or_none()
            return document
        except Exception as e:
            logger.error(f"Error retrieving document {document_id}: {str(e)}")
            return None

    async def get_documents_by_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Document]:
        """Get documents for a specific user with pagination"""
        try:
            stmt = select(Document).where(Document.user_id == user_id).offset(skip).limit(limit)
            result = await self.db_session.execute(stmt)
            documents = result.scalars().all()
            return documents
        except Exception as e:
            logger.error(f"Error retrieving documents for user {user_id}: {str(e)}")
            return []

    async def delete_document(self, document_id: UUID) -> bool:
        """Delete a document by ID"""
        try:
            # First, delete associated chunks
            stmt = delete(DocumentChunk).where(DocumentChunk.document_id == document_id)
            await self.db_session.execute(stmt)
            
            # Then delete the document
            stmt = delete(Document).where(Document.id == document_id)
            result = await self.db_session.execute(stmt)
            
            if result.rowcount > 0:
                await self.db_session.commit()
                logger.info(f"Document {document_id} deleted successfully")
                return True
            else:
                await self.db_session.rollback()
                logger.warning(f"Document {document_id} not found for deletion")
                return False
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {str(e)}")
            await self.db_session.rollback()
            return False

    async def add_chunks_to_document(self, document_id: UUID, chunks_data: List[dict]) -> bool:
        """Add chunks to an existing document"""
        try:
            # Verify document exists
            document = await self.get_document_by_id(document_id)
            if not document:
                raise ValueError(f"Document with ID {document_id} does not exist")
            
            # Create chunk instances
            chunks = []
            for chunk_data in chunks_data:
                chunk = DocumentChunk(
                    id=uuid.uuid4(),
                    document_id=document_id,
                    content=chunk_data["content"],
                    chunk_order=chunk_data["chunk_order"],
                    chunk_metadata=chunk_data.get("metadata"),
                    embedding_id=chunk_data["embedding_id"],
                    token_count=chunk_data.get("token_count", len(chunk_data["content"].split()))
                )
                chunks.append(chunk)
            
            # Add chunks to session
            self.db_session.add_all(chunks)
            await self.db_session.commit()
            
            logger.info(f"Added {len(chunks)} chunks to document {document_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding chunks to document {document_id}: {str(e)}")
            await self.db_session.rollback()
            raise

    async def get_document_chunks(self, document_id: UUID) -> List[DocumentChunk]:
        """Get all chunks for a specific document"""
        try:
            stmt = select(DocumentChunk).where(DocumentChunk.document_id == document_id).order_by(DocumentChunk.chunk_order)
            result = await self.db_session.execute(stmt)
            chunks = result.scalars().all()
            return chunks
        except Exception as e:
            logger.error(f"Error retrieving chunks for document {document_id}: {str(e)}")
            return []

    async def process_and_chunk_document(self, document_id: UUID, max_tokens: int = 1000, overlap: int = 100) -> bool:
        """Process and chunk an existing document according to specified parameters"""
        try:
            # Get the document
            document = await self.get_document_by_id(document_id)
            if not document:
                raise ValueError(f"Document with ID {document_id} does not exist")

            # Initialize document processor
            processor = DocumentProcessor()

            # Process the document content
            result = processor.process_document_content(document.content, document.source_type)
            chunks_data = result["chunks"]

            # Prepare chunks for database insertion
            chunks_to_add = []
            for chunk_data in chunks_data:
                chunk = DocumentChunk(
                    id=uuid.uuid4(),
                    document_id=document_id,
                    content=chunk_data["content"],
                    chunk_order=chunk_data["chunk_order"],
                    metadata="",  # We could store additional metadata here
                    embedding_id="",  # This will be set when embeddings are generated
                    token_count=chunk_data["token_count"]
                )
                chunks_to_add.append(chunk)

            # Add all chunks to the session
            self.db_session.add_all(chunks_to_add)
            await self.db_session.commit()

            logger.info(f"Successfully processed and chunked document {document_id} into {len(chunks_data)} chunks")
            return True
        except Exception as e:
            logger.error(f"Error processing and chunking document {document_id}: {str(e)}")
            await self.db_session.rollback()
            raise

    async def extract_document_metadata(self, document_id: UUID) -> Optional[Dict]:
        """Extract and return metadata for a specific document"""
        try:
            document = await self.get_document_by_id(document_id)
            if not document:
                return None

            # Initialize document processor
            processor = DocumentProcessor()

            # Extract metadata
            metadata = processor.extract_metadata(document.content, document.source_type, document.title)

            return metadata
        except Exception as e:
            logger.error(f"Error extracting metadata for document {document_id}: {str(e)}")
            return None