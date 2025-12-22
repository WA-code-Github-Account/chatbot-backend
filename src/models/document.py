from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from config.database import Base
from datetime import datetime
import uuid


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    doc_metadata = Column(String, nullable=True)  # JSON string - renamed from 'metadata'
    upload_date = Column(DateTime, default=datetime.utcnow)
    source_type = Column(String(50), nullable=False)  # PDF, text, web page, etc.
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    page_count = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Document(id={self.id}, title={self.title})>"