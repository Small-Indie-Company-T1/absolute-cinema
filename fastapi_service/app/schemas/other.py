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

class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None
    status_code: int
