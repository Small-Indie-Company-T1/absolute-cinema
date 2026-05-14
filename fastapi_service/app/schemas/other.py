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
    duration: int
    genres: List[GenreOut]

class MovieList(BaseModel):
    id: int
    title: str
    release_date: date
    description: str
    genres: List[GenreOut]

class ErrorDetail(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    detail: ErrorDetail
