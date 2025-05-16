from users.serializer import UserSerializer
from rest_framework import generics


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
