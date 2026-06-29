from datetime import timedelta

from celery import shared_task
import datetime
from users.models import CustomUser
from django.utils import timezone
from django.db.models import Q


@shared_task
def block_inactive_users():
    now = timezone.now()
    month_ago = now - timedelta(days=30)
    inactive_users = CustomUser.objects.filter(is_active=True).filter(
        Q(last_login__lt=month_ago)
        | (Q(last_login__isnull=True) & Q(date_joined__lt=month_ago))
    )

    inactive_users.update(is_active=False)
    print("Пользователи, не заходившие более месяца - заблокированы")
