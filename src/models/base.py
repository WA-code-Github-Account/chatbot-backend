from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func
from config.database import Base


class TimestampMixin:
    """Mixin class to add created_at and updated_at timestamps to models"""
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BaseModel(Base):
    """Base model that other models can inherit from"""
    __abstract__ = True
    
    # Include the timestamp mixin by default
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())