from sqlalchemy import exc
from fastapi import APIRouter, HTTPException, status

from app.config import create_access_token
from app.user.auth import get_password_hash
from app.user.dao import UsersDAO
from app.user.schemas import UserSchemaRegister


router = APIRouter(prefix='/auth', tags=['Регистрация/Авторизация'])


@router.post("/register/")
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
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль',
        )
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}
