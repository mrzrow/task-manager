from pydantic import BaseModel
from typing import TYPE_CHECKING
from datetime import datetime


class TaskBase(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    due_date: datetime | None = None
    user_id: int


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


TaskBase.model_rebuild()
