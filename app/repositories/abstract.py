from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Type
from pydantic import BaseModel
from sqlalchemy.sql import Select
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T", bound=BaseModel)


class GenericRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        raise NotImplementedError()

    @abstractmethod
    async def list(self, **filters) -> list[T]:
        raise NotImplementedError()

    @abstractmethod
    async def add(self, record: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, record: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError()


class GenericSqlRepository(GenericRepository[T], ABC):

    def __init__(self, session: AsyncSession, model_cls: Type[T]) -> None:
        self._session = session
        self._model_cls = model_cls

    def _construct_get_stmt(self, id: int) -> Select:
        stmt = select(self._model_cls).where(self._model_cls.id == id)
        return stmt

    async def get_by_id(self, id: int) -> Optional[T]:
        stmt = self._construct_get_stmt(id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    def _construct_list_stmt(self, **filters) -> Select:
        stmt = select(self._model_cls)
        where_clauses = []
        for c, v in filters.items():
            if not hasattr(self._model_cls, c):
                raise ValueError(f"Invalid column name {c}")
            where_clauses.append(getattr(self._model_cls, c) == v)

        if len(where_clauses) == 1:
            stmt = stmt.where(where_clauses[0])
        elif len(where_clauses) > 1:
            stmt = stmt.where(and_(*where_clauses))
        return stmt

    async def list(self, **filters) -> list[T]:
        stmt = self._construct_list_stmt(**filters)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def add(self, record: T) -> T:
        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        return record

    async def update(self, record: T) -> T:
        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        return record

    async def delete(self, id: int) -> None:
        record = await self.get_by_id(id)
        if record is not None:
            await self._session.delete(record)
            await self._session.flush()
