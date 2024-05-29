from enum import Enum

from pydantic import BaseModel, Field


class StatusType(Enum):
    FREE = False
    PENDING = True


class CreateTableSchema(BaseModel):
    table_number: int = Field(ge=1)
    capacity: int = Field(ge=1)


class ChangeTableSchema(CreateTableSchema):
    status: bool = False

