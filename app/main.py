from fastapi import FastAPI

from app.student.router import router as students_router
from app.major.router import router as majors_router
from app.user.router import router as users_router

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Привет, мир!"}

app.include_router(students_router)
app.include_router(majors_router)
app.include_router(users_router)
