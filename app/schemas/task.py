from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TaskBase(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    due_date: datetime | None = None
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class TaskGetById(TaskBase):
    id: int


class TaskGetByUserId(TaskBase):
    user_id: int


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool
    due_date: datetime | None = None
    user_id: int


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    due_date: datetime | None = None
    user_id: int | None = None


class TaskDelete(BaseModel):
    id: int
