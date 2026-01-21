from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from infrastructure.config import confisettings


class Database:
    def __init__(self, url: str):
        self.engine = create_async_engine(url)
        self.sessionmaker = async_sessionmaker(autocommit=False, expire_on_commit=False, bind=self.engine)


database = Database(confisettings.db.url())


async def get_db():
    db = database.sessionmaker()
    try:
        yield db
    finally:
        await db.close()


async_context_db = asynccontextmanager(get_db)
