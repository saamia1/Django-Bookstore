from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from books.models import Book, Author, Category  # Import only the models that are in books/models.py
from cart.models import Cart, CartItem  # Import Cart and CartItem from cart/models.py
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class BookTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.author = Author.objects.create(name='Author 1')
        self.category = Category.objects.create(name='Category 1')
        self.book = Book.objects.create(
            title='Book 1',
            author=self.author,
            published_date='2024-01-01',
            isbn='1234567890123',
            category=self.category
        )

    def test_create_book(self):
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': self.author.id,
            'published_date': '2024-01-01',
            'isbn': '1234567890124',
            'category': self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'New Book')

    def test_get_books(self):
        url = reverse('book-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        data = {
            'title': 'Updated Book',
            'author': self.author.id,
            'published_date': '2024-01-01',
            'isbn': '1234567890123',
            'category': self.category.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(id=self.book.id).title, 'Updated Book')

    def test_delete_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
