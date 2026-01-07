from pydantic import BaseModel, Field
from sqlalchemy.engine import url
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import UTC, datetime

from src.domain.entity import Summary
from src.infrastructure.repository.summary import SummaryRepository


class CreateSummaryData(BaseModel):
    title: str = Field(max_length=200, default="")
    author: str = Field(default="")
    url: str = Field(default="")
    content: str = Field(max_length=500, default="")
    keywords: list[str]
    published_at: str


class SummaryService:
    def __init__(self, session: AsyncSession):
        self.session = session

        self._summary_repo = SummaryRepository(session)

    async def create_list(
        self,
        summary_list_data: list[CreateSummaryData],
    ) -> list[Summary]:
        return await self._summary_repo.bulk(
            [
                Summary(
                    title=summary.title,
                    author=summary.author,
                    url=summary.url,
                    content=summary.content,
                    keywords=summary.keywords,
                    published_at=datetime.strptime(
                        summary.published_at, "%a, %d %b %Y %H:%M:%S %z"
                    ).astimezone(UTC),
                )
                for summary in summary_list_data
            ]
        )
