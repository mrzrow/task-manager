from fastapi import Depends

from app.services.user import UserService
from app.utils.unit_of_work import UnitOfWork
from app.depends.unit_of_work import get_unit_of_work


def get_user_service(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> UserService:
    return UserService(uow)
