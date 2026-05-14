from typing import List

from pydantic import BaseModel

from app.schemas.other import MovieOut


class RecommendationItem(BaseModel):
    movie: MovieOut
    score: float
    reason: str

class RecommendationResponse(BaseModel):
    items: List[RecommendationItem]

class RebuildRecommendationRequest(BaseModel):
    user_id: int

class RebuildRecommendationResponse(BaseModel):
    status: str
    message: str
