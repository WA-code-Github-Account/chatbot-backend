from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from config.database import Base
from datetime import datetime
import uuid


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
    chunk_order = Column(Integer, nullable=False)  # Order number of this chunk in the document
    chunk_metadata = Column(String, nullable=True)  # JSON string for chunk-specific metadata - renamed from 'metadata'
    embedding_id = Column(String, nullable=False)  # ID in Qdrant vector database
    token_count = Column(Integer, nullable=True)  # Number of tokens in the chunk

    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, document_id={self.document_id}, order={self.chunk_order})>"