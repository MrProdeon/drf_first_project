from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import SET_NULL, CASCADE
from datetime import date
from teaching.models import Course, Lesson


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None

    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Город", blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, verbose_name="Аватар")

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Payments(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=CASCADE, verbose_name="Пользователь")
    payment_date = models.DateField(verbose_name="Дата оплаты", default=date.today)
    course = models.ForeignKey(Course, on_delete=CASCADE, null=True, blank=True, verbose_name="Курс")
    lesson = models.ForeignKey(Lesson, on_delete=CASCADE, null=True, blank=True, verbose_name="Урок")
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")

    session_id = models.CharField(max_length=400, verbose_name="id сессии", blank=True, null=True)
    payment_link = models.TextField(verbose_name="Ссылка на оплату", blank=True, null=True)

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "наличные"
        TRANSFER = "transfer", "перевод"

    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)

    def clean(self):
        if not self.course and not self.lesson:
            raise ValidationError("Должен быть указан либо курс, либо урок")
        if self.course and self.lesson:
            raise ValidationError("Нельзя указать и курс, и урок одновременно")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
