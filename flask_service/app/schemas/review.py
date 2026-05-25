from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class ReviewCreate(BaseModel):
    """Схема для создания отзыва"""

    movie_id: int
    user_id: int
    rating: int = Field(..., ge=1, le=10)
    text: str = Field(..., min_length=1, max_length=1000)

    @field_validator("text")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v.strip()


class ReviewResponse(BaseModel):
    """Схема ответа с отзывом"""

    id: int
    movie_id: int
    user_id: int
    rating: int
    text: str
    status: str
    created_at: str


class ReviewStatusUpdate(BaseModel):
    """Схема для обновления статуса отзыва"""

    status: Literal["active", "hidden"]


class ErrorResponse(BaseModel):
    """Единый формат ошибок"""

    status: str = "error"
    error: dict = Field(...)

    @staticmethod
    def build(code: str, message: str, details: Any = None) -> dict:
        """Вспомогательная функция для создания ошибки"""
        payload: dict = {"status": "error", "error": {"code": code, "message": message}}
        if details is not None:
            payload["error"]["details"] = details
        return payload
