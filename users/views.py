from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from teaching.paginators import ProjectPagination
from users.models import CustomUser, Payments
from users.serializers import UserSerializer, PaymentSerializer

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = ProjectPagination

class UserCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class PaymentViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    pagination_class = ProjectPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["payment_date"]
    filterset_fields = ["course", "lesson", "payment_method"]