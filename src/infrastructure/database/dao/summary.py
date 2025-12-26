from sqlalchemy import (
    ARRAY,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.dao.base import Base


class Summary(Base):
    __tablename__ = "summary"

    id: Mapped[int] = mapped_column("summary_id", primary_key=True)
    content: Mapped[str] = mapped_column("content", String(500), nullable=False)
    keyword: Mapped[list[str]] = mapped_column("keyword", ARRAY(String), nullable=True)
