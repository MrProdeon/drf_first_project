from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from teaching.models import Course, Lesson
from teaching.serializers import CourseSerializer, LessonSerializer
from rest_framework import generics

from users.permissions import IsModerator, IsNotModerator, IsOwner


# Create your views here.
class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer

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
