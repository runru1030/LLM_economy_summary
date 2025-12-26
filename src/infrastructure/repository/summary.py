from src.domain.entity import Summary
from src.infrastructure.repository.base import BaseMapper
from src.infrastructure.database.dao import (
    SummaryDao,
)


class SummaryMapper(BaseMapper):
    @staticmethod
    def entity_to_dao(entity: Summary) -> SummaryDao:
        return SummaryDao(**entity.model_dump())

    @staticmethod
    def dao_to_entity(dao: SummaryDao) -> Summary:
        return Summary.model_validate(dao.model_dump())
