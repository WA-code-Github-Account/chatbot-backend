from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from config.database import Base
from datetime import datetime
import uuid


class UserQuery(Base):
    __tablename__ = "user_queries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_text = Column(Text, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    response = Column(Text, nullable=True)
    source_citations = Column(String, nullable=True)  # JSON string
    response_time_ms = Column(Integer, nullable=True)  # Time taken to generate response
    language = Column(String(10), nullable=False, default='en')  # 'en' or 'ur'

    def __repr__(self):
        return f"<UserQuery(id={self.id}, user_id={self.user_id}, timestamp={self.timestamp})>"