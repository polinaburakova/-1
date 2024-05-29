import uuid

from sqlalchemy import Column, UUID, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    table_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    date = Column(DateTime, nullable=False)
