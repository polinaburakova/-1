import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateOrderSchema(BaseModel):
    table_id: uuid.UUID
    date: datetime


class UpdateOrderSchema(BaseModel):
    table_id: Optional[uuid.UUID]
