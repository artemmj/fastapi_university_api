from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.file.router import router as files_router
from app.major.router import router as majors_router
from app.pages.router import router as pages_router
from app.student.router import router as students_router
from app.user.router import router as users_router

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Привет, мир!"}

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(files_router)
app.include_router(users_router)
app.include_router(majors_router)
app.include_router(students_router)
app.include_router(pages_router)
