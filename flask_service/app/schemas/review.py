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


class ErrorResponse(BaseModel):
    """Единый формат ошибок"""

    error: str
    detail: str | None = None
    status_code: int
