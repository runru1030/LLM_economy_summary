from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class IBaseRepository(ABC, Generic[T]):  # pragma: no cover
    @staticmethod
    def combine_where(model, query, kwargs):
        for key, value in kwargs.items():
            if isinstance(value, list):
                query = query.where(getattr(model, key).in_(value))
            else:
                query = query.where(getattr(model, key) == value)  # type: ignore

        return query

    @abstractmethod
    def __init__(self, *args, **kwargs): ...

    @abstractmethod
    async def find_by(self, **kwargs) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def delete_by(self, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def partial_update_by(self, update_data: dict, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, *args, **kwargs) -> T:
        raise NotImplementedError

    @abstractmethod
    async def insert(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def bulk(self, entities: list[T]):
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: T):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity: T):
        raise NotImplementedError
