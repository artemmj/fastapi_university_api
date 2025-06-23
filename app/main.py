import os
from typing import List

from fastapi import FastAPI

from app.models import Student
from utils import json_to_dict_list

path_to_json = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'students.json')

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привет, мир!"}

@app.get("/students", response_model=List[Student] | None)
def get_all_students(
    course: int | None = None,
    major: str | None = None,
    enrollment_year: int | None = None,
):
    students = json_to_dict_list(path_to_json)
    if not course and not major and not enrollment_year:
        return students

    return_students = []
    if students and course:
        for student in students:
            if student.course == course:
                return_students.append(student)
    if major:
        return_students = [student for student in return_students if student['major'].lower() == major.lower()]
    if enrollment_year:
        return_students = [student for student in return_students if student['enrollment_year'] == enrollment_year]
    return return_students

@app.get("/students/{id}", response_model=Student)
def get_student_by_id(id: int):
    students = json_to_dict_list(path_to_json)
    for student in students:
        if student["id"] == id:
            return student
    return "Не найдено"
