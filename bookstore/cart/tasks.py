from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_purchase_confirmation_email(user_email, cart_items):
    subject = 'Purchase Confirmation'
    message = f'Thank you for your purchase! You have bought: {", ".join(cart_items)}.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
