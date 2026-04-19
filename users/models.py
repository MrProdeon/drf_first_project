from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    username = None

    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Город", blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, verbose_name="Аватар")

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"