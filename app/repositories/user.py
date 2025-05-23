from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from .abstract import GenericRepository, GenericSqlRepository
from app.models.user import User


class UserRepositoryBase(GenericRepository[User], ABC):
    pass


class UserRepository(GenericSqlRepository[User], UserRepositoryBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
    