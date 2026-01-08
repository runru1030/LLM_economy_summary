from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.base.repository import IBaseRepository
from src.domain.entity import Summary
from src.infrastructure.repository.base import BaseMapper
from src.infrastructure.database.dao import (
    SummaryDao,
)
from sqlalchemy.dialects.postgresql import insert


class SummaryMapper(BaseMapper):
    @staticmethod
    def entity_to_dao(entity: Summary) -> SummaryDao:
        return SummaryDao(**entity.model_dump())

    @staticmethod
    def dao_to_entity(dao: SummaryDao) -> Summary:
        return Summary.model_validate(dao)


class SummaryRepository(IBaseRepository[Summary]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by(self, **kwargs) -> list[Summary]:
        query = self.combine_where(
            SummaryDao,
            select(SummaryDao),
            kwargs,
        )
        return [
            SummaryMapper.dao_to_entity(x)
            for x in (await self.session.scalars(query)).unique()
        ]

    async def find_deleted(self) -> list[Summary]:
        pass

    async def delete_by(self, **kwargs) -> None:
        raise NotImplementedError

    async def partial_update_by(self, update_data: dict, **kwargs) -> None:
        query = self.combine_where(
            SummaryDao, update(SummaryDao).values(update_data), kwargs
        )
        await self.session.execute(query)

    async def find_by_id(self, summary_id: int) -> Summary:
        query = select(SummaryDao).where(SummaryDao.id == summary_id)
        dao = (await self.session.scalars(query)).unique().one()
        return SummaryMapper.dao_to_entity(dao)

    async def insert(self, entity: Summary) -> Summary:
        project_dao = SummaryMapper.entity_to_dao(entity)
        self.session.add(project_dao)
        await self.session.flush()

        return SummaryMapper.dao_to_entity(project_dao)

    async def bulk(self, entities: list[Summary]) -> None:
        values = [SummaryMapper.entity_to_dao(entity) for entity in entities]
        stmt = insert(SummaryDao).values(values)
        stmt = stmt.on_conflict_do_nothing(index_elements=["url"])
        self.session.execute(stmt)

    async def update(self, entity: Summary):
        summary_dao = SummaryMapper.entity_to_dao(entity)
        query = (
            update(SummaryDao)
            .values(summary_dao)
            .where(SummaryDao.id == summary_dao.id)
        )
        await self.session.execute(query)

    async def delete(self, entity: Summary):
        await self.session.execute(delete(SummaryDao).where(SummaryDao.id == entity.id))
