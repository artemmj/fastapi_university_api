import httpx
from datetime import date
from pydantic import ValidationError

from app.models import Student


def get_all_students():
    url = "http://127.0.0.1:8000/students"
    response = httpx.get(url)
    return response.json()

students = get_all_students()

def test_valid_student(data: dict) -> None:
    try:
        Student(**data)
    except ValidationError as e:
        print(f"Ошибка валидации: {e}")

student_data = {
    "student_id": 1,
    "phone_number": "+1234567890",
    "first_name": "Иван",
    "last_name": "Иванов",
    "date_of_birth": date(2000, 1, 1),
    "email": "ivan.ivanov@example.com",
    "address": "Москва, ул. Пушкина, д. Колотушкина",
    "enrollment_year": 2022,
    "major": "Программирование",
    "course": 3,
    "special_notes": "Увлекается программированием"
}

test_valid_student(student_data)
