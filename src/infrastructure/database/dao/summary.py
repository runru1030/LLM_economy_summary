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
    title: Mapped[str] = mapped_column("title", String(200), nullable=False)
    content: Mapped[str] = mapped_column("content", String(500), nullable=False)
    keywords: Mapped[list[str]] = mapped_column(
        "keywords", ARRAY(String), nullable=True
    )
    author: Mapped[str] = mapped_column("author", String(200), nullable=False)
    published_at: Mapped[datetime] = mapped_column(
        "published_at",
        UTCTimestamp,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at",
        UTCTimestamp,
        server_default=text("CURRENT_TIMESTAMP"),
    )
