from django.db import models
from django.db.models import SET_NULL, CASCADE


# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(verbose_name="Превью(картинка)", null=True, blank=True)
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(verbose_name="Превью(картинка)")
    description = models.TextField(verbose_name="Описание")
    video_url = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(to=Course, on_delete=CASCADE, verbose_name="курс")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"