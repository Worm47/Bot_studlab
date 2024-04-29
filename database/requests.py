from database.models import async_session
from database.models import User
from sqlalchemy import select


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_current_command(tg_id: int, command: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            user.current_command = command
            session.add(user)
            await session.commit()

async def set_base_city(tg_id: int, command: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            user.base_city = command
            session.add(user)
            await session.commit()

async def set_base_news(tg_id: int, command: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            user.base_news = command
            session.add(user)
            await session.commit()

async def set_base_joke(tg_id: int, command: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            user.base_joke = command
            session.add(user)
            await session.commit()

async def get_user_settings(tg_id: int) -> tuple[str, str, str]:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user.base_city, user.base_news, user.base_joke
        return "Омск", "technology", "программисты"
