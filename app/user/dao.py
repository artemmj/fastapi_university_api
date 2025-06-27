from app.dao.base import BaseDAO

from app.user.models import User


class UsersDAO(BaseDAO):
    model = User
