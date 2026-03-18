from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class RequestAudit(Base):
    __tablename__ = "request_audits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symptom_description: Mapped[str] = mapped_column(Text, nullable=False)
    top_specialty: Mapped[str | None] = mapped_column(String(255), nullable=True)
    response_time_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    prompt_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cache_hits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cache_misses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    red_flag_triggered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    samu_advised: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)