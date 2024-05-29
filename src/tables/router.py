import uuid

from fastapi import APIRouter, Depends, HTTPException

from src.auth.db import User
from src.auth.manager import fastapi_users
from src.auth.schemas import RoleType
from src.tables.db import DB
from src.tables.schemas import CreateTableSchema, ChangeTableSchema

router = APIRouter(
    prefix="/tables",
    tags=["tables"]
)


current_user = fastapi_users.current_user()
db = DB()


@router.post('/create')
async def create_table(data: CreateTableSchema, user: User = Depends(current_user)):
    if user.role == RoleType.ADMIN.value:
        return await db.create_table(data.dict())
    raise HTTPException(status_code=400, detail="permission denied")


@router.get('/all')
async def all_tables():
    return await db.get_all_tables()


@router.get('/{table_id}')
async def get_table(table_id: uuid.UUID):
    return await db.get_table(table_id)


@router.delete('/{table_id}')
async def delete_table(table_id: uuid.UUID, user: User = Depends(current_user)):
    if user.role == RoleType.ADMIN.value:
        await db.delete_table(table_id)
        return {'id': table_id}
    raise HTTPException(status_code=400, detail="permission denied")


@router.put('/{table_id}')
async def update_table(table_id: uuid.UUID, data: ChangeTableSchema, user: User = Depends(current_user)):
    if user.role == RoleType.ADMIN.value:
        return await db.update_table(table_id, data.dict())
    raise HTTPException(status_code=400, detail="permission denied")
