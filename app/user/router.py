from sqlalchemy import exc
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.config import create_access_token
from app.user.auth import get_password_hash, authenticate_user
from app.user.dao import UsersDAO
from app.user.dependencies import get_current_user, get_current_admin_user
from app.user.schemas import UserSchemaRegister, UserSchemaAuth
from app.user.models import User


router = APIRouter(prefix='/auth', tags=['Авторизация'])


@router.post("/register", summary="Регистрация")
async def register_user(reg_data: UserSchemaRegister) -> dict:
    user_dict = reg_data.dict()
    user_dict['password'] = get_password_hash(reg_data.password)
    try:
        await UsersDAO.create(**user_dict)
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Невозможно зарегистрироваться с переданными данными'
        )
    return {'message': 'Вы успешно зарегистрированы'}


@router.post("/login", summary="Авторизация")
async def auth_user(response: Response, user_data: UserSchemaAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль',
        )
    access_token = create_access_token({"sub": str(check.id)})
    # response используется для управления HTTP-ответом, отправляемым клиенту
    # httponly указывает, что куки доступны только через HTTP(S), и не доступны скриптам JavaScript на клиенте
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


@router.post("/logout", summary="Разлогиниться")
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get("/me", summary="Инфо о юзере")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.get("/all_users/")
async def get_all_users(user_data: User = Depends(get_current_admin_user)):
    return await UsersDAO.get_all()
