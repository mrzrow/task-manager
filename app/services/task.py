from app.utils.unit_of_work import UnitOfWork
from app.models.task import Task
from app.schemas.task import (
    TaskCreate,
    TaskBase,
    TaskGetById,
    TaskUpdate,
    TaskDelete
)

class TaskService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_task(self, task_create: TaskCreate) -> TaskBase:
        task_data = task_create.model_dump()
        task = Task(**task_data)
        task = await self.uow.task.add(task)
        await self.uow.commit()
        return TaskBase.model_validate(task, from_attributes=True)

    async def get_task_by_id(self, task_id: TaskGetById) -> TaskBase | None:
        task_id = task_id.id
        task = await self.uow.task.list(id=task_id)
        if not task:
            return None
        return TaskBase.model_validate(task[0], from_attributes=True)
    
    async def get_tasks(self) -> list[TaskBase]:
        tasks = await self.uow.task.list()
        return [TaskBase.model_validate(task, from_attributes=True) for task in tasks]
    
    async def update_task(self, task_update: TaskUpdate) -> TaskBase | None:
        task_id = task_update.id
        task = await self.uow.task.list(id=task_id)
        if not task:
            return None
        task_data = task_update.model_dump()
        for key, value in task_data.items():
            setattr(task, key, value)
        await self.uow.commit()
        return TaskBase.model_validate(task, from_attributes=True)
    
    async def delete_task(self, task_delete: TaskDelete) -> None:
        task_id = task_delete.id
        await self.uow.task.delete(id=task_id)
        await self.uow.commit()
