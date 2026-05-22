from typing import List

from app.services.client_service import CatalogClient
from app.schemas.other import MovieOut
from app.schemas.search import SearchResult


class SearchService:
    def __init__(self, client_service: CatalogClient):
        self.client_service = client_service

    async def filter_movies(
        self,
        movies: List[MovieOut],
        genre_id: int | None,
        year_from: int | None,
        year_to: int | None
    ) -> List[MovieOut]:
        filtered: List[MovieOut] = []

        for movie in movies:
            if genre_id is not None:
                genre_ids = {genre.id for genre in movie.genres}
                if genre_id not in genre_ids:
                    continue

            release_year = movie.release_date.year

            if year_from is not None and release_year < year_from:
                continue

            if year_to is not None and release_year > year_to:
                continue
            
            filtered.append(movie)
        return filtered

    def text_search(
        self,
        movies: List[MovieOut],
        q: str,
        limit: int
    ) -> List[MovieOut]:
        q_norm = q.lower().strip()
        scored = []
        for movie in movies:
            title = movie.title.lower()
            desc = movie.description.lower()
            score = 0
            if q_norm in title:
                score += 10
                if title.startswith(q_norm):
                    score += 5
            if q_norm in desc:
                score += 3
            if score > 0:
                scored.append((movie, score))
        scored.sort(key=lambda item: (item[1], item[0].release_date), reverse=True)
        return [movie for movie, _ in scored[:limit]]

    async def search_movies(
        self,
        q: str | None = None,
        genre_id: int | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        limit: int = 10
    ) -> SearchResult:
        movies = await self.client_service.get_all_movies()

        filtered = await self.filter_movies(movies, genre_id, year_from, year_to)

        if q:
            items = self.text_search(filtered, q, limit)
        else:
            sorted_movies = sorted(
                filtered,
                key=lambda movie: movie.release_date,
                reverse=True
            )
            items = sorted_movies[:limit]
        
        return SearchResult(items=items, total=len(items))
