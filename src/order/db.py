import uuid

from config import async_session_maker
from src.order.models import OrderModel
from src.tables.db import DB as TableDB
from src.tables.schemas import StatusType

from sqlalchemy import select, delete, update


class DB:
    def __init__(self):
        self.session = async_session_maker()
        self.table_db = TableDB()

    async def create_order(self, data: dict) -> dict:
        order = OrderModel(**data)
        self.session.add(order)

        table = await self.table_db.get_table(order.table_id)

        table['status'] = StatusType.PENDING.value

        await self.table_db.update_table(order.table_id, table)
        await self.session.commit()

        return {
            'id': order.id,
            'user_id': order.user_id,
            'table_id': order.table_id,
            'date': order.date
        }

    async def get_orders(self) -> list[dict]:
        orders = await self.session.execute(select(OrderModel))

        return [{
            'id': row[0].id,
            'user_id': row[0].user_id,
            'table_id': row[0].table_id,
            'date': row[0].date
        } for row in orders]

    async def get_order(self, order_id: uuid.UUID) -> dict:
        order = await self.session.execute(select(OrderModel).where(OrderModel.id == order_id))
        row = order.fetchone()

        if row is None:
            return {}

        return {
            'id': row[0].id,
            'user_id': row[0].user_id,
            'table_id': row[0].table_id,
            'date': row[0].date
        }

    async def delete_order(self, order_id: uuid.UUID):
        order = OrderModel(**await self.get_order(order_id))
        await self.session.execute(delete(OrderModel).where(OrderModel.id == order_id))
        await self.session.commit()

        table = await self.table_db.get_table(order.table_id)
        table['status'] = StatusType.FREE.value

        await self.table_db.update_table(order.table_id, table)

    async def update_order(self, order_id: uuid.UUID, data: dict) -> dict:
        await self.session.execute(update(OrderModel).where(OrderModel.id == order_id).values(**data))
        await self.session.commit()

        if 'table_id' in data:
            table = await self.table_db.get_table(data['table_id'])
            table['status'] = not table['status']

            await self.table_db.update_table(table['id'], table)

        return await self.get_order(order_id)
