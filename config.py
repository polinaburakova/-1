from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DB_NAME = "database.db"
DATABASE_URL = f"sqlite+aiosqlite:///./{DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
