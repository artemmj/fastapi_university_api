from typing import Optional

from pydantic import BaseModel, Field


class MajorSchemaGet(BaseModel):
    id: int = Field(...)
    major_name: str = Field(..., description="Название факультета")
    major_description: str = Field(None, description="Описание факультета")
    count_students: int = Field(0, description="Количество студентов")


class MajorSchemaAdd(BaseModel):
    # Не указываем id, так как БД автоматически сформирует его
    major_name: str = Field(..., description="Название факультета")
    major_description: str = Field(None, description="Описание факультета")
    count_students: int = Field(0, description="Количество студентов")


class MajorSchemaUpdate(BaseModel):
    major_name: Optional[str] = Field(None, description="Новое название факультета")
    major_description: Optional[str] = Field(None, description="Новое описание факультета")
