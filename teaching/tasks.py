from celery import shared_task
from django.core.mail import send_mail

from teaching.models import Course
from config import settings


@shared_task
def send_information_about_update(course_id: int, recipient_list: list[str]) -> None:
    course = Course.objects.get(pk=course_id)

    send_information = {
        "subject": f"Курс {course.title} получил обновление!",
        "message": f"Вы подписаны на обновление курса {course.title}. Рады сообщить, что курс обновлен."
        f" Узнайте что нового в числе первых! ",
        "from_email": settings.DEFAULT_FROM_EMAIL,
        "recipient_list": recipient_list,
    }

    send_mail(**send_information)
