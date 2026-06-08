from django.core.management.base import BaseCommand
from teaching.models import Course, Lesson
from users.models import Payments, CustomUser


class Command(BaseCommand):
    help = "Add test payments to the database"

    def handle(self, *args, **options):
        CustomUser.objects.all().delete()
        Payments.objects.all().delete()

        users_data = [
            {
                "phone_number": "89377012108",
                "city": "Volzsky",
                "email": "prodeon21@gmail.com",
            },
            {
                "phone_number": "89377013535",
                "city": "Volgograd",
                "email": "testuser@gmail.com",
            },
        ]

        user_objects = {}

        for user_data in users_data:
            user, created = CustomUser.objects.get_or_create(**user_data)
            user_objects[user.email] = user
            if created:
                print(f"Пользователь {user.email} успешно создан!")
            else:
                print(f"Пользователь {user.email} уже есть!")

        course, course_created = Course.objects.get_or_create(
            title="Python Basic",
            defaults={
                "description": "Базовый курс по Python для начинающих"
            }
        )

        if course_created:
            print(f"Курс '{course.title}' успешно создан!")
        else:
            print(f"Курс '{course.title}' уже существует!")

        lesson, lesson_created = Lesson.objects.get_or_create(
            title="Введение в Python",
            course=course,
            defaults={
                "description": "Первый урок по основам Python",
                "video_url": "https://www.youtube.com/watch?v=example"
            }
        )

        if lesson_created:
            print(f"Урок '{lesson.title}' успешно создан!")
        else:
            print(f"Урок '{lesson.title}' уже существует!")

        payments_data = [
            {
                "user": user_objects["prodeon21@gmail.com"],
                "payment_amount": 1000,
                "payment_method": "transfer",
                "course": course,
                "lesson": None,
                "payment_date" : "2025-03-26"
            },
            {
                "user": user_objects["prodeon21@gmail.com"],
                "payment_amount": 2000,
                "payment_method": "cash",
                "course": None,
                "lesson": lesson,
                "payment_date" : "2024-03-26"
            },
            {
                "user": user_objects["testuser@gmail.com"],
                "payment_amount": 1500,
                "payment_method": "transfer",
                "course": course,
                "lesson": None
            },
        ]

        for payment_data in payments_data:
            try:
                filtered_data = {k: v for k, v in payment_data.items() if v is not None}
                payment, created = Payments.objects.get_or_create(**filtered_data)
                if created:
                    print(f"Платеж на сумму {payment.payment_amount} успешно создан!")
                else:
                    print(f"Платеж на сумму {payment.payment_amount} уже существует!")
            except Exception as e:
                print(f"Произошла ошибка: {e}")