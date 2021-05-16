from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer

UserModel: User = get_user_model()


class CreateUserView(CreateAPIView):
    model = UserModel
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class RetrieveUserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    model = UserModel
    serializer_class = UserSerializer

    def get_object(self):
        try:
            return self.request.user
        except UserModel.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
