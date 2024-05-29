import uuid

from config import async_session_maker
from src.tables.models import TableModel

from sqlalchemy import select, delete, update


class DB:
    def __init__(self):
        self.session = async_session_maker()

    # Добавить столик
    async def create_table(self, data: dict) -> dict:
        table = TableModel(**data)
        self.session.add(table)
        await self.session.commit()

        return {
            'id': table.id,
            'table_number': table.table_number,
            'capacity': table.capacity,
            'status': table.status
        }

    async def get_table(self, table_id: uuid.UUID) -> dict:
        table = await self.session.execute(select(TableModel).where(TableModel.id == table_id))
        row = table.fetchone()

        if row is None:
            return {}

        return {
            'id': row[0].id,
            'table_number': row[0].table_number,
            'capacity': row[0].capacity,
            'status': row[0].status
        }

    async def delete_table(self, table_id: uuid.UUID):
        await self.session.execute(delete(TableModel).where(TableModel.id == table_id))
        await self.session.commit()

    async def get_all_tables(self) -> list[dict]:
        tables = await self.session.execute(select(TableModel))

        return [{
            'id': row[0].id,
            'table_number': row[0].table_number,
            'capacity': row[0].capacity,
            'status': row[0].status
        } for row in tables]

    async def update_table(self, table_id: uuid.UUID, data: dict) -> dict:
        await self.session.execute(update(TableModel).where(TableModel.id == table_id).values(**data))
        await self.session.commit()
        return await self.get_table(table_id)

    async def check_table(self, table_id: uuid.UUID) -> bool:
        tb = await self.get_table(table_id)
        return tb['status']
