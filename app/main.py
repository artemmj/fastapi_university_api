from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.file.router import router as files_router
from app.major.router import router as majors_router
from app.pages.router import router as pages_router
from app.student.router import router as students_router
from app.user.router import router as users_router

app = FastAPI()
templates = Jinja2Templates(directory='app/templates')

@app.get("/")
async def reg_page(request: Request):
    return templates.TemplateResponse(
        name='registration.html',
        context={
            'request': request,
        },
    )

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(files_router)
app.include_router(users_router)
app.include_router(majors_router)
app.include_router(students_router)
app.include_router(pages_router)
