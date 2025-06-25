from fastapi import APIRouter, Depends

from app.student.dao import StudentDAO
from app.student.rb import RBStudent
from app.student.schemas import StudentSchemaGet, StudentSchemaCreate

router = APIRouter(prefix='/students', tags=['Работа со студентами'])


@router.get("/", summary="Получить всех", response_model=list[StudentSchemaGet])
async def get_all_students(request_body: RBStudent = Depends()):
    return await StudentDAO.get_all(**request_body.to_dict())


@router.get(
    path="/{id}",
    summary="Получить по айди",
    response_model=StudentSchemaGet | dict,
)
async def get_student_by_id(id: int):
    result = await StudentDAO.get_by_id(id)
    if not result:
        return {"message": "Not found"}
    return result


@router.post("/", summary="Добавить нового")
async def create_student(student: StudentSchemaCreate) -> dict:
    check = await StudentDAO.create(**student.dict())
    if check:
        return {"message": "Студент успешно добавлен!", "student": student}
    else:
        return {"message": "Ошибка при добавлении студента!"}
