from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entity import Summary
from src.infrastructure.repository.summary import SummaryRepository


class CreateSummaryData(BaseModel):
    content: str = Field(max_length=500, default="")
    keywords: list[str]


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
                Summary(content=summary.content, keywords=summary.keywords)
                for summary in summary_list_data
            ]
        )
