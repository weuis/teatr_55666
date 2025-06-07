from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from main_service.models import Genre, Actor, Play
from main_service.serializer import GenreSerializer, ActorSerializer, PlaySerializer

User = get_user_model()

class ModelTests(TestCase):
    def test_genre_str(self):
        genre = Genre.objects.create(name="Comedy")
        self.assertEqual(str(genre), "Comedy")

    def test_actor_str(self):
        actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.assertEqual(str(actor), "John Doe")

    def test_play_str_and_relations(self):
        genre = Genre.objects.create(name="Drama")
        actor = Actor.objects.create(first_name="Jane", last_name="Smith")
        play = Play.objects.create(title="Hamlet", description="A tragedy")
        play.genres.add(genre)
        play.actors.add(actor)
        self.assertEqual(str(play), "Hamlet")
        self.assertIn(genre, play.genres.all())
        self.assertIn(actor, play.actors.all())

class SerializerTests(TestCase):
    def test_genre_serializer(self):
        genre = Genre.objects.create(name="Comedy")
        serializer = GenreSerializer(genre)
        self.assertEqual(serializer.data['name'], "Comedy")

    def test_actor_serializer(self):
        actor = Actor.objects.create(first_name="John", last_name="Doe")
        serializer = ActorSerializer(actor)
        self.assertEqual(serializer.data['first_name'], "John")
        self.assertEqual(serializer.data['last_name'], "Doe")

    def test_play_serializer_create(self):
        genre = Genre.objects.create(name="Drama")
        actor = Actor.objects.create(first_name="Jane", last_name="Smith")
        data = {
            "title": "Hamlet",
            "description": "A tragedy",
            "genres": [genre.id],
            "actors": [actor.id]
        }
        serializer = PlaySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        play = serializer.save()
        self.assertEqual(play.title, "Hamlet")
        self.assertIn(genre, play.genres.all())
        self.assertIn(actor, play.actors.all())

class ViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.genre = Genre.objects.create(name="Comedy")
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.client.login(username='testuser', password='password')

    def test_genre_list_create(self):
        # GET /genres/
        url = reverse('main_service:genre-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

        # POST /genres/
        response = self.client.post(url, {"name": "Drama"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Drama")

    def test_actor_list_search(self):
        # GET /actors/?search=John
        url = reverse('main_service:actor-list')
        response = self.client.get(url, {"search": "John"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['first_name'], "John")

    def test_play_create_and_retrieve(self):
        # POST /plays/
        url = reverse('main_service:play-list')
        response = self.client.post(url, {
            "title": "Hamlet",
            "description": "A tragedy",
            "genres": [self.genre.id],
            "actors": [self.actor.id]
        }, format='json')
        self.assertEqual(response.status_code, 201)
        play_id = response.data["id"]

        # GET /plays/{id}/
        detail_url = reverse('main_service:play-detail', args=[play_id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Hamlet")


    def test_reservation_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(reverse('main_service:reservation-list'), {}, format='json')
        response = self.client.get(reverse('main_service:reservation-list'))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 0)

