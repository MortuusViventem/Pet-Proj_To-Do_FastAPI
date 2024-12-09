from pydantic import BaseModel, ConfigDict


class STaskAdd(BaseModel):
    task_name: str
    description: str | None = None


class STaskUpdate(STaskAdd):
    id: int
    task_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class STaskId(BaseModel):
    ok: bool = True
    task_id: int


class STaskOwner(BaseModel):
    id: int


class STask(BaseModel):
    id: int
    task_name: str
    description: str | None = None
    status: bool = False

    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    id: int
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserInDB(User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
