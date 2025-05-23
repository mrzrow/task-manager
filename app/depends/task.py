from fastapi import Depends

from app.utils.unit_of_work import UnitOfWork
from app.services.task import TaskService
from app.depends.unit_of_work import get_unit_of_work


def get_task_service(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> TaskService:
    return TaskService(uow)
