import os
from jose import jwt
from datetime import datetime, timedelta, timezone
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

s = Settings()

def get_db_url():
    return f"postgresql+asyncpg://{s.DB_USER}:{s.DB_PASSWORD}@{s.DB_HOST}:{s.DB_PORT}/{s.DB_NAME}"

def get_auth_data():
    return {"secret_key": s.SECRET_KEY, "algorithm": s.ALGORITHM}

def create_access_token(data: dict) -> str:
    """Функция создает JWT токен для аутентификации пользователей."""
    to_encode = data.copy()
    # Задаем время жизни токена
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    # Получаем данные из настроек - секретный ключи и алгоритм шифрования
    auth_data = get_auth_data()
    # Кодируем все данные в JWT
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt
