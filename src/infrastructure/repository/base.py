from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class BaseMapper(ABC, Generic[T, U]):
    @staticmethod
    @abstractmethod
    def entity_to_dao(entity: T) -> U:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def dao_to_entity(dao: U) -> T:
        raise NotImplementedError
