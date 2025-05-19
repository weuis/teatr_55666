from users.serializer import UserSerializer
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LoginUserView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES