from datetime import UTC, datetime
from pydantic import BaseModel, Field, ConfigDict


class Summary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    content: str
    title: str
    keywords: list[str]
    author: str
    published_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
