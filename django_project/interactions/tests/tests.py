from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from interactions.domain.models import Watchlist
from catalog.domain.models import Movie
from interactions.services.services import (
    add_movie_to_watchlist,
    remove_movie_from_watchlist,
)
from interactions.domain.exceptions import MovieAlreadyInWatchlist, MovieNotFound


User = get_user_model()


class WatchlistServiceTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="example@email", password="pass12345"
        )
        self.movie = Movie.objects.create(
            title="Movie 1",
            description="pPrive",
            release_date="2024-01-01",
            duration=120,
        )

    def test_add_movie_to_watchlist_success(self):
        add_movie_to_watchlist(self.user, self.movie.id)
        self.assertTrue(
            Watchlist.objects.filter(user=self.user, movie=self.movie).exists()
        )

    def test_add_movie_to_watchlist_raises_movie_not_found(self):
        with self.assertRaises(MovieNotFound):
            add_movie_to_watchlist(self.user, 999999)

    def test_add_movie_to_watchlist_raises_duplicate(self):
        Watchlist.objects.create(user=self.user, movie=self.movie)
        with self.assertRaises(MovieAlreadyInWatchlist):
            add_movie_to_watchlist(self.user, self.movie.id)

    def test_remove_movie_from_watchlist_success(self):
        Watchlist.objects.create(user=self.user, movie=self.movie)
        remove_movie_from_watchlist(self.user, self.movie.id)
        self.assertFalse(
            Watchlist.objects.filter(user=self.user, movie=self.movie).exists()
        )

    def test_remove_movie_from_watchlist_raises_if_not_exists(self):
        with self.assertRaises(MovieNotFound):
            remove_movie_from_watchlist(self.user, self.movie.id)


class WatchlistApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="example@email", password="pass12345"
        )
        self.other_user = User.objects.create_user(
            email="example@email2", password="pass12345"
        )
        self.movie1 = Movie.objects.create(
            title="Movie 1",
            description="pPrive",
            release_date="2024-01-01",
            duration=120,
        )
        self.movie2 = Movie.objects.create(
            title="Movie 2",
            description="pPrive",
            release_date="2024-01-01",
            duration=120,
        )

        self.list_url = reverse("watchlist-list")
        self.add_url = reverse("watchlist-add-to-watchlist")
        self.remove_url = reverse("watchlist-remove-from-watchlist")

    def test_auth_required(self):
        response = self.client.post(
            self.add_url, {"movie": self.movie1.id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_to_watchlist_success(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.add_url, {"movie": self.movie1.id}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Watchlist.objects.filter(user=self.user, movie=self.movie1).exists()
        )

    def test_add_to_watchlist_duplicate(self):
        self.client.force_authenticate(self.user)
        Watchlist.objects.create(user=self.user, movie=self.movie1)

        response = self.client.post(
            self.add_url, {"movie": self.movie1.id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_from_watchlist_success(self):
        self.client.force_authenticate(self.user)
        Watchlist.objects.create(user=self.user, movie=self.movie1)

        response = self.client.post(
            self.remove_url, {"movie": self.movie1.id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Watchlist.objects.filter(user=self.user, movie=self.movie1).exists()
        )

    def test_mark_as_watched_success(self):
        self.client.force_authenticate(self.user)
        item = Watchlist.objects.create(
            user=self.user, movie=self.movie1, watched=False
        )
        mark_url = reverse("watchlist-mark-as-watched", args=[item.id])

        response = self.client.post(mark_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item.refresh_from_db()
        self.assertTrue(item.watched)

    def test_cannot_mark_other_user_item(self):
        self.client.force_authenticate(self.user)
        other_item = Watchlist.objects.create(
            user=self.other_user,
            movie=self.movie2,
            watched=False,
        )
        mark_url = reverse("watchlist-mark-as-watched", args=[other_item.id])

        response = self.client.post(mark_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_watched_true(self):
        self.client.force_authenticate(self.user)
        Watchlist.objects.create(user=self.user, movie=self.movie1, watched=True)
        Watchlist.objects.create(user=self.user, movie=self.movie2, watched=False)

        response = self.client.get(self.list_url + "?watched=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_ordering_added_at(self):
        self.client.force_authenticate(self.user)
        Watchlist.objects.create(user=self.user, movie=self.movie1, watched=False)
        Watchlist.objects.create(user=self.user, movie=self.movie2, watched=True)

        response = self.client.get(self.list_url + "?ordering=-added_at")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
