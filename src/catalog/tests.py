from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Movie, Genre


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
