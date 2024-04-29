from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)  # Используем явное указание типа
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)  # Тип данных BigInteger
    current_command: Mapped[str] = mapped_column(String, nullable=True)  # Строка для текущей команды
    base_city: Mapped[str] = mapped_column(String, nullable=True)  # Строка для текущей команды
    base_news: Mapped[str] = mapped_column(String, nullable=True)  # Строка для текущей команды
    base_joke: Mapped[str] = mapped_column(String, nullable=True)  # Строка для текущей команды



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)