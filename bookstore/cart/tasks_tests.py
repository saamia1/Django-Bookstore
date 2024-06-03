# cart/tasks_tests.py

from django.test import TestCase
from unittest.mock import patch
from .tasks import send_purchase_confirmation_email

class TaskTests(TestCase):
    @patch('cart.tasks.send_mail')
    def test_send_purchase_confirmation_email(self, mock_send_mail):
        user_email = 'test@example.com'
        cart_items = ['Book 1', 'Book 2']
        send_purchase_confirmation_email(user_email, cart_items)
        mock_send_mail.assert_called_once_with(
            'Purchase Confirmation',
            'Thank you for your purchase! You have bought: Book 1, Book 2.',
            'your-email@gmail.com',
            [user_email],
            fail_silently=False,
        )
