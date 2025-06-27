from datetime import datetime, timezone
from jose import jwt, JWTError
from fastapi import Request, HTTPException, status, Depends

from app.config import get_auth_data
# from app.exceptions import TokenExpiredException, NoJwtException, NoUserIdException, ForbiddenException
from app.user.dao import UsersDAO
from app.user.models import User


def get_token(request: Request):
    """Функция пытается получить токен их запроса."""
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не найден')
    return token


async def get_current_user(token: str = Depends(get_token)):
    """Фукнция проверяет срок действия токена и возвращает юзера если все ок."""
    try:
        # Декодер - чтобы получить из токена данные с которыми можно будет работать (exp и sub)
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    # Проверка срока действия токена, если истек - выбрасываем исключение
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

    user = await UsersDAO.get_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь не найден')

    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    """Фукнция либо возвращает пользователя если он админ, либо выбросит исключение."""
    if current_user.is_admin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')
