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
        if user.groups.filter(name="moderators").exists():
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

class LessonRetriveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method in ["DELETE", "PUT", "PATCH"]:
            return [IsOwner(), IsAuthenticated()]
        else:
            return [IsAuthenticated()]

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

        return Response({"message" : message}, status=status.HTTP_201_CREATED)


