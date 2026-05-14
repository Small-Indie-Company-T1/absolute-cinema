from fastapi import APIRouter, Query

from app.schemas.search import SearchResult
from app.services.client_service import CatalogClient
from app.services.search_service import SearchService
from app.core.config import settings


router = APIRouter(prefix='/api/v1')
catalog_client = CatalogClient(settings.BASE_URL)
search_service = SearchService(catalog_client)


@router.get('/search', response_model=SearchResult)
async def search_movies(
    q: str | None = Query(default=None, min_length=1, max_length=100),
    genre_id: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    limit: int = Query(default=10, ge=1, le=50)
):
    return await search_service.search_movies(
        q=q,
        genre_id=genre_id,
        year_from=year_from,
        year_to=year_to,
        limit=limit
    )