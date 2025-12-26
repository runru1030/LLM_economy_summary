from datetime import UTC, datetime
from pydantic import BaseModel, Field


class Summary(BaseModel):
    id: int | None = None
    content: str
    keywords: list[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
