from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from teaching.models import Course
from teaching.paginators import ProjectPagination
from teaching.services import create_stripe_product, create_stripe_price, create_stripe_session
from users.models import CustomUser, Payments
from users.serializers import UserSerializer, PaymentSerializer
from utils.docs_examples import example_user_dict, example_payments_dict
from utils.common_errors import common_errors


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = ProjectPagination
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Получить список пользователей (с учетом прав доступа)",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Успешный ответ со списком пользователей',
                schema=UserSerializer,
                examples={
                    'application/json': example_user_dict
                }
            ),
            **common_errors
        }
    )
    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить пользователя",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Пользователь получен',
                examples={
                    'application/json': example_user_dict
                }
            ),
            **common_errors})
    def retrieve(self, request, *args, **kwargs):
        super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать нового пользователя",
        request_body=UserSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Пользователь успешно создан',
                examples={
                    'application/json': example_user_dict
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Неверно составлен запрос",
                examples={
                    "application/json": {

                        "email": [
                            "This field is required."
                        ],
                        "password": [
                            "This field is required."
                        ]

                    }
                }
            ),
            **common_errors
        })
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Изменить пользователя",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Пользователь изменен',
                examples={
                    'application/json': example_user_dict
                }
            ),
            **common_errors})
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично изменить пользователя",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Пользователь изменен',
                examples={
                    'application/json': example_user_dict
                }
            ),
            **common_errors})
    def partial_update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить пользователя",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description='Пользователь удален',
            ),
            **common_errors})
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)


class UserCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Создать пользователя",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Пользователь создан',
                examples={
                    "application/json": {
                        **example_user_dict
                    }
                }
            ),
            **common_errors})
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)


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
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.payment_link = payment_link
        payment.save()

    @swagger_auto_schema(
        operation_description="Получить список платежей (с учетом прав доступа)",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Успешный ответ со списком платежей',
                schema=PaymentSerializer,
                examples={
                    'application/json': example_payments_dict
                }
            ),
            **common_errors
        }
    )
    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить платёж",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Платёж получен',
                examples={
                    'application/json': example_payments_dict
                }
            ),
            **common_errors})
    def retrieve(self, request, *args, **kwargs):
        super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый платёж",
        request_body=PaymentSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Платёж успешно создан',
                examples={
                    'application/json': example_user_dict
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Неверно составлен запрос",
                examples={
                    "application/json": {

                        "payment_amount": [
                            "This field is required."
                        ],
                        "payment_method": [
                            "This field is required."
                        ]

                    }
                }
            ),
            **common_errors
        })
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Изменить платёж",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Платёж изменен',
                examples={
                    'application/json': example_user_dict
                }
            ),
            **common_errors})
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично изменить платёж",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Платёж изменен',
                examples={
                    'application/json': example_user_dict
                }
            ),
            **common_errors})
    def partial_update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить платёж",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description='Платёж удален',
            ),
            **common_errors})
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)


class MyTokenObtainPairView(TokenObtainPairView):

    @swagger_auto_schema(
        operation_description="Получить токен авторизации",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Получение токена",
                examples={
                    "application/json": {
                        "refresh": "YourTokenHere",
                        "access": "YourTokenHere"
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class MyTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description="Получить обновление токена",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Получение обновления токена",
                examples={
                    "application/json": {
                        "access": "YourTokenHere"
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)