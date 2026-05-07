from django.db import models
from django.db.models import SET_NULL, CASCADE
from config import settings



# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(verbose_name="Превью(картинка)", null=True, blank=True)
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=CASCADE, null=True, blank=True, verbose_name="Владелец")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(verbose_name="Превью(картинка)", blank=True, null=True)
    description = models.TextField(verbose_name="Описание")
    video_url = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(to=Course, on_delete=CASCADE, verbose_name="курс", related_name="lessons")
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=CASCADE, null=True, blank=True, verbose_name="Владелец")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

class Subscription(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=CASCADE, verbose_name="Курс")

    def __str__(self):
        return f"Подиска {self.user.email} на курс {self.course.title}"

    class Meta:
        verbose_name = "Подиска"
        verbose_name_plural = "Подписки"