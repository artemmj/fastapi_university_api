import re
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, datetime
from typing import Optional


class Major(str, Enum):
    informatics = "Информатика"
    economics = "Экономика"
    history = "История"
    math = "Математика"
    bio = "Биология"
    eco = "Экология"
    psyho = "Психология"


class Student(BaseModel):
    id: int
    phone_number: str = Field(..., description="Номер телефона, в формате '+7ХХХХХХХХХХ'")
    last_name: str = Field(..., min_length=1, max_length=50, description="Фамилия, от 1 до 50 символов")
    date_of_birth: date = Field(..., description="Дата рождения, в формате ГГГГ-ММ-ДД")
    email: EmailStr = Field(..., description="Электронная почта")
    address: str = Field(..., min_length=10, max_length=200, description="Адрес, не более 200 символов")
    enrollment_year: int = Field(..., ge=2002, description="Год поступления, не меньше 2002")
    major: Major = Field( ..., description="Специальность")
    course: int = Field(..., ge=1, le=5, description="Курс, в диапазоне от 1 до 5")
    special_notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Дополнительные заметки, не более 500 символов",
    )

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{2,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 2 до 17 цифр')
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value: date):
        if value and value >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return value
