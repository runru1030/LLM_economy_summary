import typing
from fastapi import Depends, Query
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.query.summary import SummaryQuery
from src.infrastructure.database import get_db
from src.user_interface.restapi.dto.summary import SummaryGetV5ResponseWithPagination

summary_router = APIRouter(
    prefix="/summary",
    tags=["summary"],
)
SessionDeps = typing.Annotated[AsyncSession, Depends(get_db)]


@summary_router.get(
    "",
    response_model=SummaryGetV5ResponseWithPagination,
)
async def get_summary_list_v5(
    session: SessionDeps,
    limit: int = Query(10, description="페이지 당 데이터 개수"),
    offset: int = Query(0, description="페이지 인덱스"),
    asc: bool = Query(False, description="오름차순 정렬 여부"),
):
    return await SummaryQuery.get_list(
        session,
        offset=offset,
        limit=limit,
        asc=asc,
    )
