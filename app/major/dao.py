from app.dao.base import BaseDAO

from app.major.models import Major


class MajorDAO(BaseDAO):
    model = Major

