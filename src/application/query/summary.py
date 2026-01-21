import datetime

from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from infrastructure.database.dao import (
    SummaryDao,
)
from infrastructure.repository.summary import SummaryMapper
from user_interface.restapi.dto.summary import OrderBy


class SummaryQuery:
    @staticmethod
    async def get_list(
        session: AsyncSession,
        offset: int,
        limit: int,
        _asc: bool,
        order_by: OrderBy = OrderBy.published_at,
    ):
        subq = select(SummaryDao.url, func.max(SummaryDao.id).label("max_id")).group_by(SummaryDao.url).subquery()
        base_query = select(SummaryDao).where(SummaryDao.id == subq.c.max_id)
        total_count = await session.scalar(select(func.count()).select_from(base_query.subquery()))

        order_column: InstrumentedAttribute[datetime]
        match order_by:
            case OrderBy.created_at:
                order_column = SummaryDao.created_at
            case OrderBy.published_at:
                order_column = SummaryDao.published_at
        query = base_query.order_by(asc(order_column) if _asc else desc(order_column)).offset(offset).limit(limit)
        result_set = await session.scalars(query)
        summaries = [SummaryMapper.dao_to_entity(dao).model_dump() for dao in result_set]

        return {
            "total": total_count or 0,
            "offset": offset,
            "limit": limit,
            "asc": _asc,  # 변수명 수정 (전달받은 bool 값 사용)
            "summaries": summaries,
        }
        rows = (await session.execute(query)).unique().all()[offset : offset + limit]
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
