from fastapi import APIRouter

from app.schemas.recommendations import RecommendationResponse
from app.services import recommendations_service


router = APIRouter(prefix='/api/v1')

@router.get('/recommendations/similar/{movie_id}', response_model=RecommendationResponse)
async def similar_movies(movie_id: int, limit: int = 10):
    return await recommendations_service.get_similar_movies(...)
