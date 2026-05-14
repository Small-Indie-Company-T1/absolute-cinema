from typing import Tuple

from pydantic import BaseModel

from app.schemas.other import MovieShortOut


class RecommendationItem(BaseModel):
    movie: MovieShortOut
    score: float
    reason: str

class RecommendationResponse(BaseModel):
    items: Tuple[RecommendationItem]

class RebuildRecommendationRequest(BaseModel):
    user_id: int

class RebuildRecommendationResponse(BaseModel):
    status: str
    message: str
