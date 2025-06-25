from sqlalchemy import (
    event,
    select as sqlalchemy_select,
    update as sqlalchemy_update,
)
from sqlalchemy.orm import joinedload

from app.database import async_session_maker
from app.student.models import Student
from app.major.models import Major


class StudentDAO:

    @classmethod
    async def get_all(cls, **filters):
        async with async_session_maker() as session:
            query = sqlalchemy_select(Student).options(joinedload(Student.major)).filter_by(**filters)
            students = await session.execute(query)
            sstudents = students.scalars().all()

            return_students = []
            for student in sstudents:
                student_data = student.to_dict()
                student_data['major'] = student.major.major_name
                return_students.append(student_data)
            return return_students

    @classmethod
    async def get_by_id(cls, id: int):
        async with async_session_maker() as session:
            query = sqlalchemy_select(Student).options(joinedload(Student.major)).filter_by(id=id)
            result = await session.execute(query)
            student_info = result.scalar_one_or_none()

            if not student_info:
                return None

            student_data = student_info.to_dict()
            student_data['major'] = student_info.major.major_name
            return student_data

    @classmethod
    async def create(cls, data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                new_student = Student(**data)
                session.add(new_student)
                await session.flush()
                new_student_id = new_student.id
                await session.commit()
                return new_student_id


@event.listens_for(Student, 'after_insert')
def upd_major_after_insert(mapper, connection, target):
    major_id = target.major_id
    connection.execute(
        sqlalchemy_update(Major)
        .where(Major.id == major_id)
        .values(count_students=Major.count_students + 1)
    )
