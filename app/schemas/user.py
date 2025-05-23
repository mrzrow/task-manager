from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserGetById(BaseModel):
    id: int


class UserCreate(BaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None


class UserDelete(BaseModel):
    id: int


class UserUpdate(BaseModel):
    id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
