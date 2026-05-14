from typing import List

import httpx

from app.schemas.other import MovieList, MovieOut
from app.core.exceptions.movie_exceptions import MovieNotFound
from app.core.exceptions.client_exceptions import CatalogClientError


class CatalogClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    async def get_movie(self, movie_id: int) -> MovieOut:
        url = f'{self.base_url}/api/movies/{movie_id}/'
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)

        if response.status_code == 404:
            raise MovieNotFound(f'Movie {movie_id} not found')

        if response.is_error:
            raise CatalogClientError(f'Catalog service returned {response.status_code}')

        data = response.json()
        return MovieOut.model_validate(data)

    async def get_all_movies(self) -> MovieList:
        url = f'{self.base_url}/api/movies/'
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
        return [MovieList.model_validate(movie) for movie in all_movies]
        