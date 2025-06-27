from fastapi import APIRouter, Request, Depends, UploadFile
from fastapi.templating import Jinja2Templates

from app.student.router import get_all_students

router = APIRouter(prefix='/pages', tags=['Фронтенд'])
templates = Jinja2Templates(directory='app/templates')


@router.get('/students')
async def get_students_html(request: Request, students=Depends(get_all_students)):
    # Тут смысл в том, что мы возвращаем не простой JSON (dict), а HTML страницу.
    # Передается объект request, что позволяет шаблону использовать его
    # для различных целей, и так же передавать какие-то свои данные
    return templates.TemplateResponse(
        name='students.html',
        context={
            'request': request,
            'students': students,
        },
    )
