from sqlalchemy import (
    select as sqlalchemy_select,
    update as sqlalchemy_update,
    delete as sqlalchemy_delete,
)

from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            query = sqlalchemy_select(cls.model)
            results = await session.execute(query)
            return results.scalars().all()

    @classmethod
    async def get_one_or_none(cls, filters: dict):
        async with async_session_maker() as session:
            query = sqlalchemy_select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_by_id(cls, id: int):
        async with async_session_maker() as session:
            query = sqlalchemy_select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def update(cls, id: int, **values):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    # Запрос на обновление записей в таблице
                    sqlalchemy_update(cls.model)
                    # Фильтрация по айди, чтобы обновить нужную запись
                    .where(cls.model.id == id)
                    # Устанавливаются новые значения для обновляемых записей
                    .values(**values)
                    # Синхронизировать состояние сессии с БД после выполнения запроса
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

    @classmethod
    async def delete(cls, id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy_delete(cls.model).filter_by(id=id)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount
