from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Author
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class AuthorTests(APITestCase):
    # Setup method to create necessary objects for tests
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a token for the user
        self.token = Token.objects.create(user=self.user)
        # Set token in client credentials for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # Create a test author
        self.author = Author.objects.create(name='Author 1')

    # Test case to create a new author
    def test_create_author(self):
        url = reverse('author-list')  # Get the URL for creating authors
        data = {'name': 'New Author'}  # Data for creating a new author
        # Send POST request to create a new author
        response = self.client.post(url, data, format='json')
        # Check if author creation was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if the number of authors in the database increased by 1
        self.assertEqual(Author.objects.count(), 2)
        # Check if the name of the newly created author matches the provided name
        self.assertEqual(Author.objects.get(id=response.data['id']).name, 'New Author')

    # Test case to retrieve all authors
    def test_get_authors(self):
        url = reverse('author-list')  # Get the URL for retrieving authors
        # Send GET request to retrieve all authors
        response = self.client.get(url, format='json')
        # Check if the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test case to update an existing author
    def test_update_author(self):
        url = reverse('author-detail', kwargs={'pk': self.author.id})  # Get the URL for updating the author
        data = {'name': 'Updated Author'}  # Data for updating the author
        # Send PUT request to update the author
        response = self.client.put(url, data, format='json')
        # Check if the update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the name of the updated author matches the provided name
        self.assertEqual(Author.objects.get(id=self.author.id).name, 'Updated Author')

    # Test case to delete an author
    def test_delete_author(self):
        url = reverse('author-detail', kwargs={'pk': self.author.id})  # Get the URL for deleting the author
        # Send DELETE request to delete the author
        response = self.client.delete(url)
        # Check if the deletion was successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check if the number of authors in the database is now 0
        self.assertEqual(Author.objects.count(), 0)
