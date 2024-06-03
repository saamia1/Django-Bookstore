from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from unittest.mock import patch
from cart.tasks import send_purchase_confirmation_email
from cart.models import Cart, CartItem
from books.models import Book, Author, Category

class UserTests(APITestCase):
    def setUp(self):
        # Set up test environment
        self.client = APIClient()  # Initialize API client for testing
        self.client.defaults['HTTP_HOST'] = 'localhost:8000'  # Set default host for client
        self.username = 'testuser'  # Define username for test user
        self.password = 'testpass'  # Define password for test user
        self.email = 'test@example.com'  # Define email for test user
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email)  # Create test user
        self.client.force_authenticate(user=self.user)  # Authenticate client with test user

    def tearDown(self):
        # Clean up after each test
        User.objects.filter(username=self.username).delete()  # Delete test user from database

    def test_create_user(self):
        # Test case to create a new user
        url = reverse('register')  # Get URL for user registration
        data = {'username': 'newuser', 'password': 'newpass', 'email': 'new@example.com'}  # Define data for creating a new user
        response = self.client.post(url, data, format='json')  # Send POST request to create a new user
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Check if user creation was successful
        self.assertEqual(User.objects.count(), 2)  # Including the user created in setUp
        self.assertEqual(User.objects.get(username='newuser').username, 'newuser')  # Check if the new user was created successfully

    def test_login_user(self):
        # Test case to authenticate user login
        User.objects.create_user(username='testuser', password='testpass', email='test@example.com')  # Create test user
        url = reverse('login')  # Get URL for user login
        data = {'username': 'testuser', 'password': 'testpass'}  # Define data for user login
        response = self.client.post(url, data, format='json')  # Send POST request to authenticate user login
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check if login was successful
        self.assertIn('token', response.data)  # Check if authentication token is present in response data

    def test_protected_endpoint(self):
        # Test case to access protected endpoint
        user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')  # Create test user
        self.client.force_authenticate(user=user)  # Authenticate client with test user
        url = reverse('profile')  # Get URL for accessing user profile
        response = self.client.get(url)  # Send GET request to access user profile
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check if request was successful
        self.assertEqual(response.data['username'], 'testuser')  # Check if correct user profile is returned

    def test_create_user_with_existing_username(self):
        # Test case to create a user with an existing username
        url = reverse('register')  # Get URL for user registration
        data = {'username': 'testuser', 'password': 'testpass', 'email': 'test2@example.com'}  # Define data for creating a new user with existing username
        response = self.client.post(url, data, format='json')  # Send POST request to create a new user
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Check if user creation failed due to existing username

    def test_create_user_with_invalid_data(self):
        # Test case to create a user with invalid data
        url = reverse('register')  # Get URL for user registration
        data = {'username': '', 'password': '', 'email': ''}  # Define invalid data for creating a new user
        response = self.client.post(url, data, format='json')  # Send POST request to create a new user
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Check if user creation failed due to invalid data

    @patch('cart.tasks.send_purchase_confirmation_email.delay')
    def test_purchase_sends_email(self, mock_send_email):
        # Test case to verify if purchase sends email
        author = Author.objects.create(name='Author Name')  # Create author for book
        category = Category.objects.create(name='Category Name')  # Create category for book
        book = Book.objects.create(title='Book Title', author=author, published_date='2023-01-01', isbn='1234567890123', category=category)  # Create book
        cart, created = Cart.objects.get_or_create(user=self.user)  # Get or create cart for user
        CartItem.objects.create(cart=cart, book=book, quantity=1)  # Add book to cart
        url = reverse('cart-purchase')  # Get URL for purchasing cart items
        response = self.client.post(url, format='json')  # Send POST request to purchase cart items
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check if purchase was successful
        mock_send_email.assert_called_once_with(self.user.email, ['Book Title'])  # Check if email was sent with correct data





