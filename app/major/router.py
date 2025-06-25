from fastapi import APIRouter

from app.major.dao import MajorDAO
from app.major.schemas import MajorSchemaGet, MajorSchemaAdd, MajorSchemaUpdate

router = APIRouter(prefix='/majors', tags=['Факультеты'])


@router.get("/", summary="Получить все", response_model=list[MajorSchemaGet])
async def get_all_students():
    return await MajorDAO.get_all()


@router.post("/", summary="Добавить новый")
async def create_new_major(major: MajorSchemaAdd) -> dict:
    check = await MajorDAO.create(**major.dict())
    if check:
        return {"message": "Факультет успешно добавлен", "major": major}
    return {"message": "Ошибка при добавлении факультета"}


@router.put("/{id}", summary="Обновить по айди")
async def update_major_description(id: int, major: MajorSchemaUpdate) -> dict:
    check = await MajorDAO.update(
        id=id,
        major_name=major.major_name,
        major_description=major.major_description,
    )
    if check:
        return {"message": "Факультет успешно обновлен", "major": major}
    return {"message": "Ошибка при обновлении факультета"}


@router.delete("/{id}", summary="Удалить по айди")
async def delete_major(id: int) -> dict:
    check = await MajorDAO.delete(id=id)
    if check:
        return {"message": f"Факультет с id={id} удален"}
    return {"message": "Ошибка при удалении факультета"}
