from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from users.serializer import UserSerializer
from django.urls import reverse

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='modeluser',
            email='model@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'modeluser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpass'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class UserSerializerTest(TestCase):
    def test_user_serializer_create(self):
        data = {
            'username': 'serialuser',
            'email': 'serial@example.com',
            'first_name': 'Serial',
            'last_name': 'User',
            'password': 'serializerpass'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, 'serialuser')
        self.assertTrue(user.check_password('serializerpass'))
        self.assertFalse(user.is_staff)

    def test_user_serializer_password_write_only(self):
        data = {
            'username': 'writeonlyuser',
            'email': 'wo@example.com',
            'first_name': 'Write',
            'last_name': 'Only',
            'password': 'pass12345'
        }
        serializer = UserSerializer(data=data)
        serializer.is_valid()
        self.assertNotIn('password', serializer.data)


class UserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.user_data = {
            'username': 'viewuser',
            'email': 'view@example.com',
            'first_name': 'View',
            'last_name': 'User',
            'password': 'viewpass123'
        }

    def test_register_view(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'viewuser')

    def test_register_missing_password(self):
        data = self.user_data.copy()
        data.pop('password')
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view_success(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, {
            'username': 'viewuser',
            'password': 'viewpass123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_view_failure(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, {
            'username': 'viewuser',
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
