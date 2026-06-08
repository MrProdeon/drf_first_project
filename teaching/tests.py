from http.client import responses

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from teaching.models import Lesson, Course, Subscription
from users.models import CustomUser
from django.urls import reverse


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email="test123@mail.ru", password="test123")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title="Test Course",
            description="Course Description",
            owner=self.user
        )
        self.lesson = Lesson.objects.create(title="test", description="test",
                                            video_url="https://www.youtube.com/watch?v=jfKfPfyJRdk",
                                            course=self.course,
                                            owner=self.user)

    def test_get(self):
        url = reverse("teaching:lessons-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 1)

    def test_retrieve(self):
        url = reverse("teaching:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], "test")

    def test_create(self):
        url = reverse("teaching:lessons-list")
        lesson_data = {
            "title": "New Lesson",
            "description": "New Description",
            "video_url": "https://www.youtube.com/watch?v=new",
            "course": self.course.id
        }
        response = self.client.post(url, lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

        second_lesson_data = {
            "title": "New Lesson",
            "description": "New Description",
            "video_url": "https://error.com",
            "course": self.course.id
        }
        second_response = self.client.post(url, second_lesson_data)
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        url = reverse("teaching:lesson-detail", args=(self.lesson.pk,))
        lesson_data = {"title": "new title"}
        response = self.client.patch(url, lesson_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], "new title")

    def test_delete(self):
        url = reverse("teaching:lesson-detail", args=(self.lesson.pk,))
        response = self.client.delete(url, args=(self.lesson.pk,))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="test_user", password="test_user")
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title="Test Course",
            description="Course Description",
            owner=self.user
        )
        #self.subscription = Subscription.objects.create(user=self.user, course=self.course)

    def test_get_subscription(self):
        url = reverse("teaching:subscriptions")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_subscription_create(self):
        url = reverse("teaching:subscriptions")
        sub_items = {"course": self.course.id}
        response = self.client.post(url, sub_items)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["message"],
                         f"Подписка пользователя {self.user.email} на курс {self.course.title} добавлена")

    def test_post_subscription_delete(self):
        url = reverse("teaching:subscriptions")
        Subscription.objects.create(course=self.course, user=self.user)
        sub_data = {"course" : self.course.id}
        response = self.client.post(url, sub_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["message"],
                         f"Подписка пользователя {self.user.email} на курс {self.course.title} удалена")