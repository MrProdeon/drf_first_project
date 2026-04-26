from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from users.models import CustomUser, Payments
from users.serializers import UserSerializer, PaymentSerializer

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class PaymentViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["payment_date"]
    filterset_fields = ["course", "lesson", "payment_method"]