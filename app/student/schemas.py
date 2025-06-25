import re
from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator


class StudentSchemaGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    email: EmailStr = Field(..., description="Электронная почта")
    first_name: str = Field(..., min_length=1, max_length=50, description="Имя, от 1 до 50 символов")
    last_name: str = Field(..., min_length=1, max_length=50, description="Фамилия, от 1 до 50 символов")
    date_of_birth: date = Field(..., description="Дата рождения в формате ГГГГ-ММ-ДД")
    address: str = Field(..., min_length=10, max_length=200, description="Адрес, не более 200 символов")
    enrollment_year: int = Field(..., ge=2002, description="Год поступления, не меньше 2002")
    major_id: int = Field(..., ge=1, description="ID факультета")
    course: int = Field(..., ge=1, le=5, description="Курс должен быть в диапазоне от 1 до 5")
    special_notes: Optional[str] = Field(None, max_length=500, description="Доп. заметки, не более 500 символов")
    major: Optional[str] = Field(..., description="Название факультета")

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if not re.match(r'^\+\d{1,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return value

    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        if value and value >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return value


class StudentSchemaCreate(BaseModel):
    # id генирирует БД
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(..., min_length=1, max_length=50, description="Имя, от 1 до 50 символов")
    last_name: str = Field(..., min_length=1, max_length=50, description="Фамилия, от 1 до 50 символов")
    date_of_birth: date = Field(..., description="Дата рождения в формате ГГГГ-ММ-ДД")
    email: EmailStr = Field(..., description="Электронная почта")
    address: str = Field(..., min_length=10, max_length=200, description="Адрес, не более 200 символов")
    enrollment_year: int = Field(..., ge=2002, description="Год поступления должен быть не меньше 2002")
    major_id: int = Field(..., ge=1, description="ID факультета")
    course: int = Field(..., ge=1, le=5, description="Курс должен быть в диапазоне от 1 до 5")
    special_notes: Optional[str] = Field(None, max_length=500, description="Доп. заметки, не более 500 символов")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{1,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value: date):
        if value and value >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return value
