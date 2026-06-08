from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from teaching.views import CourseViewSet, LessonListCreateApiView, LessonRetriveUpdateDestroyApiView, SubscriptionsAPIView

from teaching.apps import TeachingConfig

app_name = TeachingConfig.name

router = SimpleRouter()
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/", LessonListCreateApiView.as_view(), name="lessons-list"),
    path("lessons/<int:pk>/", LessonRetriveUpdateDestroyApiView.as_view(), name="lesson-detail"),
    path("subscriptions/", SubscriptionsAPIView.as_view(), name="subscriptions")

] + router.urls