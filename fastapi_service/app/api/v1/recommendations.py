from fastapi import APIRouter, BackgroundTasks, Depends, Query

from app.schemas.recommendations import RecommendationResponse, RebuildRecommendationResponse
from app.services.recommendations_service import RecommendationService
from app.services.client_service import CatalogClient, WatchlistClient
from app.core.config import settings
from app.core.auth import get_current_user, oauth2_scheme

router = APIRouter(prefix='/api/v1')
catalog_client = CatalogClient(settings.django_api_url)
watchlist_client = WatchlistClient(settings.django_api_url)
recommendation_service = RecommendationService(catalog_client, watchlist_client)


@router.get('/recommendations/similar/{movie_id}', response_model=RecommendationResponse)
async def get_similar(movie_id: int, limit: int = Query(default=10, ge=1, le=50)):
    return await recommendation_service.get_similar_movies(movie_id, limit)

@router.get('/recommendations/me', response_model=RecommendationResponse)
async def personal_recommendations(
    limit: int = Query(default=10, ge=1, le=50),
    user_id: int = Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    cached = recommendation_service.get_cached_recommendations(user_id)
    if cached is not None:
        return cached
    return await recommendation_service.get_personal_recommendations(user_id, token, limit)

@router.post('/recommendations/rebuild', response_model=RebuildRecommendationResponse)
async def rebuild_recommendations(
    background_tasks: BackgroundTasks,
    limit: int = Query(default=10, ge=1, le=50),
    user_id: int = Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    background_tasks.add_task(
        recommendation_service.rebuild_recommendations_for_user,
        user_id, token, limit
    )

    return RebuildRecommendationResponse(
        status='accepted',
        message='Recommendations rebuild started'
    )
