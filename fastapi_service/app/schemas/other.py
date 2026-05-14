from datetime import date
from typing import List

from pydantic import BaseModel


class GenreOut(BaseModel):
    id: int
    name: str

class MovieOut(BaseModel):
    id: int
    title: str
    description: str
    release_date: date
    duration: int | None = None
    poster: str | None = None
    genres: List[GenreOut]

class ErrorDetail(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    detail: ErrorDetail
