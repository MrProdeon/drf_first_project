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
from teaching.services import get_recipient_list
from teaching.tasks import send_information_about_update

from users.models import CustomUser
from users.permissions import IsModerator, IsNotModerator, IsOwner

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.common_errors import common_errors
from utils.docs_examples import example_course_dict, example_lesson_dict


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

    @swagger_auto_schema(
        operation_description="Получить список курсов (с учетом прав доступа)",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Успешный ответ со списком курсов',
                schema=LessonSerializer,
                examples={
                    'application/json': example_course_dict
                }
            ),
            **common_errors
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить курс",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Курс получен',
                examples={
                    'application/json': example_course_dict
                }
            ),
            **common_errors})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый курс",
        request_body=CourseSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Курс успешно создан',
                examples={
                    'application/json': example_course_dict
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Неверно составлен запрос",
                examples={
                    "application/json": {

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
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Изменить курс",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Курс изменен',
                examples={
                    'application/json': example_course_dict
                }
            ),
            **common_errors})
    def update(self, request, *args, **kwargs):
        course_id = kwargs.get("pk")
        recipient_list = get_recipient_list(course_id)
        send_information_about_update.delay(course_id, recipient_list)

        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Изменить курс",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Курс изменен',
                examples={
                    'application/json': example_course_dict
                }
            ),
            **common_errors})
    def partial_update(self, request, *args, **kwargs):
        course_id = kwargs.get("pk")
        recipient_list = get_recipient_list(course_id)
        send_information_about_update.delay(course_id, recipient_list)

        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить курс",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description='Курс удален',
            ),
            **common_errors})
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


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
                    'application/json': example_lesson_dict
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
                    'application/json': example_lesson_dict
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
                    'application/json': example_lesson_dict
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
                    'application/json': example_lesson_dict
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
                    'application/json': example_lesson_dict
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

    @swagger_auto_schema(
        operation_description="Создать\удалить подписку на курс. Если подписка есть - удалим её, а если её нет - добавим.",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Успешное изменение статуса подписки",
                examples={
                    "application/json":
                        {"message": "Подписка пользователя 3 на курс Основы Python удалена"}
                }
            ),
            **common_errors
        }
    )
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
