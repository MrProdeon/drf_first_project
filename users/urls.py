from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from users.views import UserViewSet, PaymentViewSet, UserCreateAPIView

from users.apps import UsersConfig

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), "register"),
    #path("login/", )
] + router.urls