import shutil

from fastapi import APIRouter, UploadFile

router = APIRouter(prefix='/files', tags=['Работа с файлами'])


@router.post('/', summary="Загрузить")
async def add_student_photo(file: UploadFile, image_name: str):
    with open(f"app/static/images/{image_name}.webp", "wb+") as photo_obj:
        shutil.copyfileobj(file.file, photo_obj)
