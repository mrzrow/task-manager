from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from app.repositories.user import UserRepositoryBase, UserRepository
from app.repositories.task import TaskRepositoryBase, TaskRepository


class UnitOfWorkBase(ABC):
    user: UserRepositoryBase
    task: TaskRepositoryBase

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()


class UnitOfWork(UnitOfWorkBase):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def __aenter__(self):
        self.user = UserRepository(self._session)
        self.task = TaskRepository(self._session)
        return self

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
