from passlib.context import CryptContext
from pydantic import EmailStr

from app.user.dao import UsersDAO

# Создание контекста для хэширования паролей,
# настраивается для использования алгоритма bcrypt.
# (deprecated="auto" указывает использовать рекомендованные
# схемы хэширования и автоматически обновлять устаревшие)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Функция для создания хэша пароля (принимает
    пароль в виде строки и возвращает его безопасный хэш).
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Функция для проверки пароля (принимает обычный пароль и его хэш,
    возвращая True, если пароль соответствует хэшу, и False в противном случае)
    """
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.get_one_or_none({"email": email})
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user
