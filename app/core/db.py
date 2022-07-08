from app.core.config import settings
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, Integer, func


class PreBase:
    """
    The extension for the base class __tablename__ and the ID
    field were created automatically.
    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


datetime_func = None
if settings.database_url.startswith('sqlite'):
    datetime_func = func.julianday
else:
    raise Exception(
        'Не определена функция извлечения времени из БД!'
    )