from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from teaching.models import Course
from teaching.paginators import ProjectPagination
from teaching.services import create_stripe_product, create_stripe_price, create_stripe_session
from users.models import CustomUser, Payments
from users.serializers import UserSerializer, PaymentSerializer

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = ProjectPagination
    permission_classes = [AllowAny]

class UserCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class PaymentViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    pagination_class = ProjectPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["payment_date"]
    filterset_fields = ["course", "lesson", "payment_method"]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = create_stripe_product(get_object_or_404(Course, id=serializer.validated_data.get("course").id))
        price = create_stripe_price(product, payment.payment_amount)
        session_id,  payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.payment_link = payment_link
        payment.save()

