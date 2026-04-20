from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from teaching.views import CourseViewSet

from teaching.apps import TeachingConfig

app_name = TeachingConfig.name

router = SimpleRouter()
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [

] + router.urls