import uuid

from fastapi import APIRouter, Depends, HTTPException, Body

from src.auth.db import User
from src.auth.manager import fastapi_users
from src.auth.schemas import RoleType
from src.order.db import DB
from src.tables.db import DB as TableDB
from src.order.schemas import CreateOrderSchema, UpdateOrderSchema

router = APIRouter(
    prefix="/order",
    tags=["orders"]
)


current_user = fastapi_users.current_user()
db = DB()
table_db = TableDB()


@router.post('/create')
async def create_order(data: CreateOrderSchema, user: User = Depends(current_user)):
    if not await table_db.check_table(data.table_id):
        return await db.create_order(data.dict() | {'user_id': user.id})
    raise HTTPException(status_code=409, detail="this table is already occupied")


@router.get('/all')
async def get_orders(user: User = Depends(current_user)):
    if user.role != RoleType.ADMIN.value:
        raise HTTPException(status_code=400, detail="permission denied")
    return await db.get_orders()


@router.get('/{order_id}')
async def get_order(order_id: uuid.UUID, user: User = Depends(current_user)):
    if user.role != RoleType.ADMIN.value:
        raise HTTPException(status_code=400, detail="permission denied")
    return await db.get_order(order_id)


@router.delete('/{order_id}')
async def delete_order(order_id: uuid.UUID, user: User = Depends(current_user)):
    if user.role == RoleType.ADMIN.value:
        await db.delete_order(order_id)
        return {'id': order_id}
    raise HTTPException(status_code=400, detail="permission denied")


@router.patch('/{order_id}')
async def update_order(order_id: uuid.UUID, data: UpdateOrderSchema = Body(...), user: User = Depends(current_user)):
    if user.role != RoleType.ADMIN.value:
        raise HTTPException(status_code=400, detail="permission denied")

    order = await db.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    old_table = await table_db.get_table(order['table_id'])

    old_table['status'] = not old_table['status']

    update_data = data.dict(exclude_unset=True)

    await table_db.update_table(order['table_id'], old_table)

    return await db.update_order(order_id, update_data)
