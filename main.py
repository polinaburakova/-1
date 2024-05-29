import sqlite3

from fastapi import FastAPI
from sqlalchemy import MetaData

from config import engine, DB_NAME
from src.auth.manager import fastapi_users, auth_backend
from src.auth.schemas import UserRead, UserCreate
from src.auth.db import Base as AuthBase
from src.tables.models import Base as TableBase
from src.order.models import Base as OrderBase
from src.tables.router import router as table_router
from src.order.router import router as order_router


def create_database(database_name: str):
    conn = sqlite3.connect(database_name)
    conn.close()


async def create_tables(*metadata: MetaData):
    async with engine.begin() as conn:
        for data in metadata:
            await conn.run_sync(data.create_all)


app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(table_router)
app.include_router(order_router)


@app.on_event("startup")
async def on_startup():
    create_database(DB_NAME)
    await create_tables(
        AuthBase.metadata,
        TableBase.metadata,
        OrderBase.metadata
    )
