from collections import Counter
import logging

from app.services.client_service import CatalogClient, WatchlistClient
from app.schemas.recommendations import RecommendationItem, RecommendationResponse

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self, catalog_service: CatalogClient, watchlist_service: WatchlistClient):
        self.catalog_service = catalog_service
        self.watchlist_service = watchlist_service
        self.cache: dict[int, list[RecommendationItem]] = {}

    async def get_similar_movies(self, target_id, limit=10):
        target = await self.catalog_service.get_movie(target_id)
        target_genres = {genre.id for genre in target.genres}
        results = []

        all_movies = await self.catalog_service.get_all_movies()
        for movie in all_movies:
            if movie.id == target.id:
                continue
            
            genre_ids = {genre.id for genre in movie.genres}
            matched = target_genres & genre_ids
            overlap = len(matched)
            if overlap > 0:
                score = float(overlap)
                target_genre_map = {genre.id: genre.name for genre in target.genres}
                matched_names = [target_genre_map[g_id] for g_id in matched]
                reason = f'Совпали жанры: {", ".join(matched_names[:3])}'
                results.append((movie, score, reason))
        
        results.sort(key=lambda item: (item[1], item[0].release_date), reverse=True)
        items=[
            RecommendationItem(
                movie=movie,
                score=score,
                reason=reason
            ) for movie, score, reason in results
        ]
        return RecommendationResponse(items=items[:limit])

    def build_genre_profile(self, watchlist):
        counter = Counter()
        for movie in watchlist:
            for genre in movie.genres:
                counter[genre.id] += 1
        return counter

    async def get_personal_recommendations(
        self, user_id: int, token: str, limit: int = 10
    ) -> RecommendationResponse:
        watchlist = await self.watchlist_service.get_watchlist_movies(token)
        excluded_ids = {movie.id for movie in watchlist}
        genre_profiles = self.build_genre_profile(watchlist)
        results = []

        all_movies = await self.catalog_service.get_all_movies()
        for movie in all_movies:
            if movie.id in excluded_ids:
                continue

            score = 0.0
            matched = []

            for genre in movie.genres:
                weight = genre_profiles.get(genre.id, 0)
                if weight:
                    score += weight
                    matched.append(genre.name)
            if score > 0:
                reason = f'Совпали жанры: {", ".join(matched[:3])}'
                item = RecommendationItem(movie=movie, score=score, reason=reason)
                results.append(item)
        results.sort(key=lambda item: (item.score, item.movie.release_date), reverse=True)
        logger.info(f'Formed recommendations for user: {user_id}')
        return RecommendationResponse(items=results[:limit])

    async def rebuild_recommendations_for_user(
        self, user_id: int, token: str, limit: int = 10
    ):
        result = await self.get_personal_recommendations(user_id=user_id, token=token, limit=limit)
        self.cache[user_id] = result.items
        return result

    def get_cached_recommendations(self, user_id: int) -> RecommendationResponse | None:
        items = self.cache.get(user_id)
        if items is None:
            return None
        return RecommendationResponse(items=items)
