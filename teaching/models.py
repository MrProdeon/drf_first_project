from django.db import models

# Create your models here.

class Course(models.Model):
    title = models.CharField(100, verbose_name="Название")
    preview = models.ImageField(verbose_name="Превью(картинка)")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

