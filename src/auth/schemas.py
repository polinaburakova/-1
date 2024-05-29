import uuid
from enum import Enum

from fastapi_users import schemas
from pydantic import BaseModel


class RoleType(Enum):
    ADMIN = "admin"
    GUEST = "guest"


class UserSchema(BaseModel):
    phone_number: str = '+79998887766'
    role: str = RoleType.ADMIN


class UserRead(schemas.BaseUser[uuid.UUID], UserSchema):
    pass


class UserCreate(schemas.BaseUserCreate, UserSchema):
    pass


class UserUpdate(schemas.BaseUserUpdate, UserSchema):
    pass
