from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from config.database import Base
from datetime import datetime
import uuid


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False)  # Unique session identifier
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)  # When the session expires
    active = Column(Boolean, default=True)  # Whether the session is still valid
    ip_address = Column(String(45), nullable=True)  # IP address from which session was created
    user_agent = Column(String(500), nullable=True)  # Browser/device info

    def __repr__(self):
        return f"<Session(id={self.id}, user_id={self.user_id}, active={self.active})>"