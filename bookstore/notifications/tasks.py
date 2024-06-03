# Import necessary modules
from celery import shared_task
from django.core.mail import send_mail
import logging

# Get logger instance
logger = logging.getLogger(__name__)

# Define shared task for sending purchase confirmation email
@shared_task
def send_purchase_confirmation_email(user_email, cart_items):
    # Define email subject and message
    subject = 'Purchase Confirmation'
    message = f'Thank you for your purchase! You have bought: {", ".join(cart_items)}.'
    
    # Log information about email being sent
    logger.info(f'Sending email to {user_email} with items: {cart_items}')
    
    # Send email using Django's send_mail function
    send_mail(subject, message, 'from@example.com', [user_email])
    
    # Log successful email sending
    logger.info('Email sent successfully')
