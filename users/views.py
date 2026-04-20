from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from users.models import CustomUser
from users.serializers import UserSerializer


# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
