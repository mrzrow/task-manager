from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from .abstract import GenericRepository, GenericSqlRepository
from app.models.task import Task


class TaskRepositoryBase(GenericRepository[Task], ABC):
    pass


class TaskRepository(GenericSqlRepository[Task], TaskRepositoryBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Task)