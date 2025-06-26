from sqlalchemy import select as sqlalchemy_select
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
from app.user.models import User


class UsersDAO:

    @classmethod
    async def get_one_or_none(cls, filters: dict):
        async with async_session_maker() as session:
            query = sqlalchemy_select(User).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_by_id(cls, id: int):
        async with async_session_maker() as session:
            query = sqlalchemy_select(User).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()


    @classmethod
    async def create(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = User(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance
