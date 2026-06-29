from drf_yasg import openapi
from rest_framework import status

# Общий словарь ответов с ошибками
common_errors = {
    status.HTTP_401_UNAUTHORIZED: openapi.Response(
        description="Не авторизован",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "detail": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        examples={
            "application/json": {
                "detail": "Authentication credentials were not provided."
            }
        },
    ),
    status.HTTP_403_FORBIDDEN: openapi.Response(
        description="Доступ запрещен",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        examples={
            "application/json": {
                "detail": "У вас недостаточно прав для выполнения этого действия."
            }
        },
    ),
}
