from datetime import datetime
from typing import Annotated
from sqlalchemy import func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import get_db_url

DATABASE_URL = get_db_url()

# Создаёт асинхронное подключение к базе данных PostgreSQL, используя драйвер asyncpg
engine = create_async_engine(DATABASE_URL)
# Создаёт фабрику асинхронных сессий, используя созданный движок.
# Сессии используются для выполнения транзакций в базе данных.
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]

# Абстрактный класс, от которого наследуются все модели. Он используется для миграций и
# аккумулирует информацию обо всех моделях, чтобы Alembic мог создавать миграции для
# синхронизации структуры базы данных с моделями на бэкенде
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    # Определяет имя таблицы для модели на основе имени класса,
    # преобразуя его в нижний регистр и добавляя букву 's'
    # в конце (например, класс User будет иметь таблицу users).
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
