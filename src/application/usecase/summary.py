from sqlalchemy.ext.asyncio import AsyncSession

from application.service.summary import CreateSummaryData, SummaryService
from application.usecase.base import BaseUseCase


class SummaryUsecase(BaseUseCase):
    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session)
        self._summary_service = SummaryService(session)

    async def create_list(
        self,
        summary_list_create_data: list[CreateSummaryData],
    ) -> None:
        return await self._summary_service.create_list(summary_list_create_data)
