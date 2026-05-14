from fastapi import APIRouter, Query

from app.schemas.recommendations import RecommendationResponse, RebuildRecommendationResponse
from app.services.recommendations_service import RecommendationService
from app.services.client_service import CatalogClient, WatchlistClient
from app.core.config import settings


router = APIRouter(prefix='/api/v1')
catalog_client = CatalogClient(settings.BASE_URL)
watchlist_client = WatchlistClient(settings.BASE_URL)
recommendation_service = RecommendationService(catalog_client, watchlist_client)


@router.get('/recommendations/similar/{movie_id}', response_model=RecommendationResponse)
async def get_similar(movie_id: int, limit: int = Query(default=10, ge=1, le=50)):
    return await recommendation_service.get_similar_movies(movie_id, limit)

@router.get('/recommendations/me', response_model=RecommendationResponse)
async def personal_recommendations(token: str, limit: int = Query(default=10, ge=1, le=50)):
    return await recommendation_service.get_personal_recommendations(token, limit)

@router.post('/recommendations/rebuild', response_model=RebuildRecommendationResponse)
async def rebuild_recommendations():
    ...
