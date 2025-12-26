from datetime import datetime
from sqlalchemy import (
    ARRAY,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.dao.base import Base, UTCTimestamp


class SummaryDao(Base):
    __tablename__ = "summary"

    id: Mapped[int] = mapped_column("summary_id", primary_key=True)
    content: Mapped[str] = mapped_column("content", String(500), nullable=False)
    keywords: Mapped[list[str]] = mapped_column(
        "keywords", ARRAY(String), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at",
        UTCTimestamp,
        server_default=text("CURRENT_TIMESTAMP"),
    )
