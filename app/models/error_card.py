from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class ErrorCard(Base):
    __tablename__ = "error_cards"
    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code            = Column(String(100), index=True)
    title           = Column(String(500), nullable=False)
    description     = Column(Text)
    category        = Column(String(50), nullable=False, index=True)
    subcategory     = Column(String(100))
    severity        = Column(String(10), nullable=False, index=True)
    causes          = Column(JSONB)
    impact          = Column(Text)
    procedure_quick = Column(JSONB)
    procedure_full  = Column(JSONB)
    commands        = Column(JSONB)
    prevention      = Column(Text)
    tags            = Column(ARRAY(String))
    aliases         = Column(ARRAY(String))
    lang_data       = Column(JSONB)
    view_count      = Column(Integer, default=0)
    resolve_count   = Column(Integer, default=0)
    is_verified     = Column(Boolean, default=False)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    updated_at      = Column(DateTime(timezone=True), onupdate=func.now())