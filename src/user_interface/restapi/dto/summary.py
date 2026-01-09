from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel
from src.application.service.summary import CreateSummaryData
from src.user_interface.restapi.dto.pagination import PaginationDto


class OrderBy(StrEnum):
    published_at = "published_at"
    created_at = "created_at"


class SummaryGetResponse(BaseModel):
    id: int
    title: str
    content: str
    keywords: list[str]
    author: str
    url: str | None
    published_at: datetime
    created_at: datetime


class SummaryGetResponseWithPagination(PaginationDto):
    summaries: list[SummaryGetResponse]


class SummaryListCreateData(BaseModel):
    summary_list: list[CreateSummaryData]
