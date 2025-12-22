from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from config.database import Base
from datetime import datetime
import uuid


class SourceCitation(Base):
    __tablename__ = "source_citations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    document_title = Column(String(255), nullable=False)
    page_number = Column(Integer, nullable=True)  # Page number in the source document
    section = Column(String(100), nullable=True)  # Section identifier in the source document
    text_preview = Column(Text, nullable=True)  # Preview text from the source
    similarity_score = Column(Integer, nullable=True)  # Similarity score of this source to the query
    query_id = Column(UUID(as_uuid=True), ForeignKey("user_queries.id"), nullable=False)  # Link to the query
    source_url = Column(String(500), nullable=True)  # URL of the source document if web-based
    source_type = Column(String(50), nullable=True)  # Type of source (web page, PDF, text, etc.)
    chunk_id = Column(String(100), nullable=True)  # ID of the chunk in the vector database
    timestamp = Column(DateTime, default=datetime.utcnow)  # When the citation was created

    def __repr__(self):
        return f"<SourceCitation(id={self.id}, document_id={self.document_id}, query_id={self.query_id})>"