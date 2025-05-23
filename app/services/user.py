from app.utils.unit_of_work import UnitOfWork
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserBase,
    UserGetById,
    UserUpdate,
    UserDelete
)


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    async def create_user(self, user_create: UserCreate) -> UserBase:
        user_data = user_create.model_dump()
        user = User(**user_data)
        user = await self.uow.user.add(user)
        await self.uow.commit()
        return UserBase.model_validate(user, from_attributes=True)
    
    async def get_user_by_id(self, user_get: UserGetById) -> UserBase | None:
        user_id = user_get.id
        user = await self.uow.user.list(id=user_id)
        if not user:
            return None
        return UserBase.model_validate(user[0], from_attributes=True)
    
    async def get_users(self) -> list[UserBase]:
        users = await self.uow.user.list()
        return [UserBase.model_validate(user, from_attributes=True) for user in users]
    
    async def update_user(self, user_update: UserUpdate) -> UserBase:
        user_id = user_update.id
        user = await self.uow.user.list(id=user_id)
        if not user:
            return None
        
        user = user[0]
        user_data = user_update.model_dump()
        for key, value in user_data.items():
            setattr(user, key, value)
        await self.uow.commit()
        return UserBase.model_validate(user, from_attributes=True)
    
    async def delete_user(self, user_delete: UserDelete) -> None:
        user_id = user_delete.id
        await self.uow.user.delete(id=user_id)
        await self.uow.commit()
