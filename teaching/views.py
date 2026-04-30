from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from teaching.models import Course, Lesson
from teaching.serializers import CourseSerializer, LessonSerializer
from rest_framework import generics

from users.permissions import IsModerator, IsNotModerator


# Create your views here.
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [IsNotModerator(), IsAuthenticated()]
        else:
            return [IsAuthenticated()]


class LessonListCreateApiView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsNotModerator(), IsAuthenticated()]
        else:
            return [IsAuthenticated()]

class LessonRetriveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsNotModerator(), IsAuthenticated()]
        else:
            return [IsAuthenticated()]
