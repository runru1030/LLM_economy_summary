from datetime import datetime
from pydantic import BaseModel
from src.application.service.summary import CreateSummaryData
from src.user_interface.restapi.dto.pagination import PaginationDto


class SummaryGetResponse(BaseModel):
    id: int
    title: str
    content: str
    keywords: list[str]
    author: str
    published_at: datetime
    created_at: datetime


class SummaryGetResponseWithPagination(PaginationDto):
    summaries: list[SummaryGetResponse]


class SummaryListCreateData(BaseModel):
    summary_list: list[CreateSummaryData]
