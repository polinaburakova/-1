from sqlalchemy import Column, UUID, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase

import uuid


class Base(DeclarativeBase):
    pass


class TableModel(Base):
    __tablename__ = "tables"
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    table_number = Column(Integer, nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False, default=False)
