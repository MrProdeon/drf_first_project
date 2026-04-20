from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from teaching.models import Course, Lesson
from teaching.serializers import CourseSerializer, LessonSerializer


# Create your views here.
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer