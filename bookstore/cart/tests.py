from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Cart, CartItem
from books.models import Book, Author, Category
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class CartTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.author = Author.objects.create(name='Author 1')
        self.category = Category.objects.create(name='Category 1')
        self.book = Book.objects.create(title='Book 1', author=self.author, published_date='2024-01-01', isbn='1234567890123', category=self.category)
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, book=self.book, quantity=1)

    def test_add_book_to_cart(self):
        url = reverse('cartitem-list')
        data = {
            'cart': self.cart.id,
            'book': self.book.id,
            'quantity': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 2)

    def test_get_cart_items(self):
        url = reverse('cartitem-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_cart_item(self):
        url = reverse('cartitem-detail', kwargs={'pk': self.cart_item.id})
        data = {
            'cart': self.cart.id,
            'book': self.book.id,
            'quantity': 2
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.get(id=self.cart_item.id).quantity, 2)

    def test_delete_cart_item(self):
        url = reverse('cartitem-detail', kwargs={'pk': self.cart_item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_purchase_cart(self):
        url = reverse('cart-purchase')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.count(), 0)
