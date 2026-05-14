from pydantic import BaseModel, Field

from app.schemas.other import MovieList


class SearchQuery(BaseModel):
    q: str | None = Field(default=None, min_length=1, max_length=100)
    genre_id: int | None = None
    year_from: int | None = Field(default=None, ge=1900, le=2100)
    year_to: int | None = Field(default=None, ge=1900, le=2100)
    limit: int = Field(default=10, ge=1, le=50)

class SearchResult(BaseModel):
    items: MovieList | list
    total: int
