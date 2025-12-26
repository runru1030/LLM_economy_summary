from pydantic import BaseModel


class PaginationDto(BaseModel):
    total: int
    offset: int
    limit: int
    asc: bool
