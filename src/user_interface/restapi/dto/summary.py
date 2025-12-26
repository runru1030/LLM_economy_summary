from datetime import datetime
from pydantic import BaseModel
from src.user_interface.restapi.dto.pagination import PaginationDto


class SummaryGetV5Response(BaseModel):
    id: int
    content: str
    keyword: list[str]
    created_at: datetime


class SummaryGetV5ResponseWithPagination(PaginationDto):
    summaries: list[SummaryGetV5Response]
