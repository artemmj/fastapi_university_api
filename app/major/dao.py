from sqlalchemy import (
    select as sqlalchemy_select,
    update as sqlalchemy_update,
    delete as sqlalchemy_delete,
)
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
from app.major.models import Major


class MajorDAO:

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            query = sqlalchemy_select(Major)
            majors = await session.execute(query)
            return majors.scalars().all()

    @classmethod
    async def create(cls, **values):
        async with async_session_maker() as session:  # Создаем асинхронную сессию
            async with session.begin():               # Начинаем транзакцию
                new_instance = Major(**values)        # Создаем новый экземпляр модели
                session.add(new_instance)             # Добавляем новый экземпляр в сессию
                try:
                    await session.commit()            # Пытаемся зафиксировать изменения в базе данных
                except SQLAlchemyError as e:
                    await session.rollback()          # В случае ошибки откатываем транзакцию
                    raise e
                return new_instance                   # Если ок, возвращаем созданный экземпляр

    @classmethod
    async def update(cls, id: int, **values):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    # Запрос на обновление записей в таблице
                    sqlalchemy_update(Major)
                    # Фильтрация по айди, чтобы обновить нужную запись
                    .where(Major.id == id)
                    # Устанавливаются новые значения для обновляемых записей
                    .values(**values)
                    # Синхронизировать состояние сессии с БД после выполнения запроса
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(query)  # Выполнение запроса на обновление
                try:
                    await session.commit()             # Сохранение изменения в базе данных
                except SQLAlchemyError as e:
                    await session.rollback()           # Если возникает ошибка, транзакция откатывается
                    raise e
                return result.rowcount                 # Возвращается количество обновлённых строк

    @classmethod
    async def delete(cls, id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy_delete(Major).filter_by(id=id)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount
