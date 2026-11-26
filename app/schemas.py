
from pydantic import BaseModel, ConfigDict


# Schema for creating a task
class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

    model_config = ConfigDict(extra="forbid")


# Schema for partially updating a task
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

    model_config = ConfigDict(extra="forbid")


# Schema for returning a task
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool

    model_config = ConfigDict(from_attributes=True)
