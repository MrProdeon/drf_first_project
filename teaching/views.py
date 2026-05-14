from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from teaching.models import Course, Lesson, Subscription
from teaching.serializers import CourseSerializer, LessonSerializer
from rest_framework import generics
from rest_framework.views import APIView
from teaching.paginators import ProjectPagination

from users.models import CustomUser
from users.permissions import IsModerator, IsNotModerator, IsOwner

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.common_errors import common_errors


# Create your views here.
class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = ProjectPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Course.objects.none()
        elif user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action == "create":
            return [IsNotModerator(), IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsOwner(), IsAuthenticated()]
        else:
            return [IsAuthenticated()]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListCreateApiView(ListCreateAPIView):
    serializer_class = LessonSerializer
    pagination_class = ProjectPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsNotModerator(), IsAuthenticated()]
        else:
            return [IsAuthenticated()]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    @swagger_auto_schema(
        operation_description="Получить список уроков (с учетом прав доступа)",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Успешный ответ со списком уроков',
                schema=LessonSerializer,
                examples={
                    'application/json': {
                        'count': 10,
                        'next': 'http://...',
                        'previous': None,
                        'results': [
                            {
                                'id': 1,
                                'title': 'Введение в Python',
                                'owner': 5,
                                'created_at': '2024-01-01T12:00:00Z'
                            }
                        ]
                    }
                }
            ),
            **common_errors
        }
    )
    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый урок",
        request_body=LessonSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Урок успешно создан',
                examples={
                    'application/json': {
                        'id': 1,
                        'title': 'Новый урок',
                        'owner': 5,
                        'created_at': '2024-01-01T12:00:00Z'
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Неверно составлен запрос",
                examples={
                    "application/json": {

                        "video_url": [
                            "This field is required."
                        ],
                        "title": [
                            "This field is required."
                        ],
                        "description": [
                            "This field is required."
                        ]

                    }
                }
            ),
            **common_errors
        })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LessonRetriveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Lesson.objects.none()
        elif user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method in ["DELETE", "PUT", "PATCH"]:
            return [IsOwner(), IsAuthenticated()]
        else:
            return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="Получить урок",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Урок получен',
                examples={
                    'application/json': {
                        "id": 0,
                        "video_url": "string",
                        "title": "string",
                        "preview": "string",
                        "description": "string",
                        "course": 0,
                        "owner": 0
                    }
                }
            ),
        **common_errors})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Полностью изменить урок",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Урок изменен',
                examples={
                    'application/json': {
                        "id": 0,
                        "video_url": "string",
                        "title": "string",
                        "preview": "string",
                        "description": "string",
                        "course": 0,
                        "owner": 0
                    }
                }
            ),
            **common_errors})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично изменить урок",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Урок изменен',
                examples={
                    'application/json': {
                        "id": 0,
                        "video_url": "string",
                        "title": "string",
                        "preview": "string",
                        "description": "string",
                        "course": 0,
                        "owner": 0
                    }
                }
            ),
            **common_errors})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить урок",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description='Урок удален',
            ),
            **common_errors})
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class SubscriptionsAPIView(APIView):
    def post(self, *args, **kwargs):

        user = self.request.user

        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(course=course_item, user=user)

        if subs_item.exists():
            subs_item.delete()
            message = f"Подписка пользователя {user.email} на курс {course_item.title} удалена"
        else:
            Subscription.objects.create(course=course_item, user=user)
            message = f"Подписка пользователя {user.email} на курс {course_item.title} добавлена"

        return Response({"message": message}, status=status.HTTP_201_CREATED)
