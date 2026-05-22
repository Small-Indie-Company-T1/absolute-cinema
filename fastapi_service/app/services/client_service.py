from typing import List

import httpx

from app.schemas.other import MovieOut
from app.core.exceptions.movie_exceptions import MovieNotFound
from app.core.exceptions.client_exceptions import CatalogClientError, WatchlistClientError


class CatalogClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    async def get_movie(self, movie_id: int) -> MovieOut:
        url = f'{self.base_url}/movies/{movie_id}/'
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)

        if response.status_code == 404:
            raise MovieNotFound(f'Movie {movie_id} not found')

        if response.is_error:
            raise CatalogClientError(f'Catalog service returned {response.status_code}')

        data = response.json()
        return MovieOut.model_validate(data)

    async def get_all_movies(self) -> List[MovieOut]:
        url = f'{self.base_url}/movies/'
        all_movies = []
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            while url:
                response = await client.get(url)
                if response.is_error:
                    raise CatalogClientError(
                        f'Catalog service returned {response.status_code}'
                    )
                data = response.json()
                if isinstance(data, dict) and 'results' in data:
                    all_movies.extend(data['results'])
                    url = data.get('next')
                elif isinstance(data, list):
                    all_movies.extend(data)
                    url = None
                else:
                    raise CatalogClientError('Unexpected catalog response format')
        return [MovieOut.model_validate(movie) for movie in all_movies]
    
class WatchlistClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    async def get_watchlist_ids(self, token: str) -> List[int]:
        url = f'{self.base_url}/interactions/watchlist/'

        movies_ids: List[int] = []

        async with httpx.AsyncClient(timeout=5.0) as client:
            while url:
                response = await client.get(
                    url,
                    headers={'Authorization': f'Bearer {token}'}
                )
                if response.is_error:
                    raise WatchlistClientError(f'Watchlist service returned {response.status_code}')
                data = response.json()
                if isinstance(data, dict) and 'results' in data:
                    results = data['results']
                    for result in results:
                        movies_ids.append(result.get('movie'))
                    url = data.get('next')
                elif isinstance(data, list):
                    movies_ids.append(data['movie'])
                    url = None
                else:
                    raise WatchlistClientError('Unexpected watchlist response format')
        return movies_ids

    async def get_watchlist_movies(self, token: str) -> List[MovieOut]:
        catalog = CatalogClient(self.base_url)
        ids = await self.get_watchlist_ids(token)
        movies = []
        for id in ids:
            movie = await catalog.get_movie(id)
            movies.append(movie)
        return movies
