from collections import Counter

from app.services.client_service import CatalogClient


class RecommendationService:
    def __init__(self, client_service: CatalogClient):
        self.client_service = client_service

    async def get_similar_movies(self, target_id, limit=10):
        target = await self.client_service.get_movie(target_id)
        target_genres = {genre.id for genre in target.genres}
        results = []

        all_movies = await self.client_service.get_all_movies()
        for movie in all_movies:
            if movie.id == target.id:
                continue
            
            genre_ids = {genre.id for genre in movie.genres}
            overlap = len(target_genres & genre_ids)
            if overlap > 0:
                score = float(overlap)
                results.append((movie, score))
        
        results.sort(key=lambda item: (item[1], item[0].release_date), reverse=True)
        return results[:limit]

    def build_genre_profile(self, watchlist):
        counter = Counter()
        for movie in watchlist:
            for genre in movie.genres:
                counter[genre.id] += 1
        return counter

    async def get_personal_recommendations(self, watchlist, limit=10):
        excluded_ids = {movie.id for movie in watchlist}
        genre_profiles = self.build_genre_profile(watchlist)
        results = []

        all_movies = await self.client_service.get_all_movies()
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
                results.append((movie, score, reason))
        results.sort(key=lambda item: (item[1], item[0].release_date), reverse=True)
        return results[:limit]
