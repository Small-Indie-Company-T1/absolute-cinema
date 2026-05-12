from unittest.mock import patch

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from catalog.domain.models import Movie, Genre
from catalog.services.services import MovieService
from catalog.domain.exceptions import MovieNotFound


class MovieApiTests(APITestCase):
    def setUp(self):
        self.genre1 = Genre.objects.create(name="Action")
        self.genre2 = Genre.objects.create(name="Drama")
        
        self.movie1 = Movie.objects.create(
            title='Movie 1',
            description='Description 1',
            release_date='2026-01-01',
            duration=120
        )
        self.movie1.genre.add(self.genre1)

        self.movie2 = Movie.objects.create(
            title='Movie 2',
            description='Description 2',
            release_date='2026-01-02',
            duration=130
        )
        self.movie2.genre.add(self.genre2)

    def test_movies_list(self):
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)

    def test_movie_detail(self):
        response = self.client.get(f'/api/movies/{self.movie1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'Movie 1')

    def test_filter_by_genre(self):
        response = self.client.get(f'/api/movies/?genre={self.genre1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_search_movies(self):
        response = self.client.get(f'/api/movies/?search=Movie 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

class MovieServiceTests(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Action')
        self.movie = Movie.objects.create(
            title='Movie 1',
            description='Description 1',
            release_date='2026-01-01',
            duration=120
        )
        self.movie.genre.add(self.genre)
        
    def test_get_all_movies_queryset(self):
        queryset = MovieService.get_all_movies()
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first(), self.movie)

    def test_get_movie_details(self):
        movie = MovieService.get_movie_details(self.movie.id)
        self.assertEqual(movie.id, self.movie.id)
        self.assertEqual(movie.title, 'Movie 1')

    def test_get_movie_details_not_found(self):
        with self.assertRaises(MovieNotFound):
            MovieService.get_movie_details(666)

class MovieApiExceptionTests(APITestCase):
    @patch("catalog.api.views.MovieService.get_all_movies")
    def test_movie_not_found(self, mocked_get_all_movies):
        mocked_get_all_movies.side_effect = MovieNotFound("Movie not found")
        response = self.client.get('/api/movies/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['code'], 404)
