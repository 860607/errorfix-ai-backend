from sqlalchemy import Column, String, Text, Float, Boolean, DateTime, SmallInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class Diagnostic(Base):
    __tablename__ = "diagnostics"
    id                = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id           = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    input_type        = Column(String(20), nullable=False)
    input_raw         = Column(Text)
    input_file_url    = Column(String(500))
    ocr_text          = Column(Text)
    error_card_id     = Column(UUID(as_uuid=True), ForeignKey("error_cards.id"), nullable=True)
    detected_system   = Column(String(100))
    detected_lang     = Column(String(10))
    confidence        = Column(Float)
    severity          = Column(String(10))
    ai_response       = Column(JSONB)
    procedure_applied = Column(JSONB)
    status            = Column(String(20), default="pending")
    user_feedback     = Column(SmallInteger)
    is_offline        = Column(Boolean, default=False)
    is_anonymous      = Column(Boolean, default=False)
    created_at        = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at       = Column(DateTime(timezone=True))