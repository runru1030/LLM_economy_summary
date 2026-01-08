from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.repository.summary import SummaryMapper
from src.infrastructure.database.dao import (
    SummaryDao,
)


class SummaryQuery:
    @staticmethod
    async def get_list(
        session: AsyncSession,
        offset: int,
        limit: int,
        asc: bool,
    ):
        base_query = (
            select(SummaryDao)
            .distinct(SummaryDao.url)
            .order_by(
                SummaryDao.url,
                SummaryDao.published_at.asc()
                if asc
                else SummaryDao.published_at.desc(),
            )
        )
        total_count: int | None = await session.scalar(
            select(func.count()).select_from(base_query)
        )

        rows = (await session.execute(base_query)).unique().all()[offset : offset + limit]
        result: dict[str, int | bool | list] = {
            "total": total_count if total_count else 0,
            "offset": offset,
            "limit": limit,
            "asc": asc,
        }
        summaries = []

        for [summary_dao] in rows:
            summary = SummaryMapper.dao_to_entity(summary_dao)
            summaries.append(summary.model_dump())

        result["summaries"] = summaries
        return result
