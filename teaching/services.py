import stripe
from django.core.mail import send_mail

from config import settings
from teaching.models import Course, Subscription

stripe.api_key = settings.STRIPE_API_KEY

def create_stripe_product(course):
    """Создает продукт в страйпе"""
    product = stripe.Product.create(
        name=course.title,
        description=course.description if course.description else None,
        metadata={
            'django_course_id': course.id,
        }
    )
    return product.id


def create_stripe_price(product_id, amount_in_cents, currency="rub"):
    """Создает цену в страйпе"""

    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount_in_cents * 100,
        currency=currency,
    )
    return price.id

def create_stripe_session(price_id):
    """Создает сессию в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        cancel_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url

def get_recipient_list(course_id : int):
    return [sub.user.email for sub in Subscription.objects.filter(course=course_id)]
