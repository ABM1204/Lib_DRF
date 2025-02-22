from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from rest_framework_simplejwt.tokens import AccessToken

from .models import Author
from rest_framework import status

User = get_user_model()


class AuthorTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="PASSWORD")
        self.client = APIClient()
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.author = Author.objects.create(
            first_name="John",
            last_name="Smith",
            date_of_birth=date(1970, 1, 1)
        )

    def test_author_list(self):
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_author_detail(self):
        response = self.client.get(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')

    def test_author_update(self):
        updated_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "biography": "New biography",
            "date_of_birth": "1980-01-01"
        }
        response = self.client.put(f'/api/authors/{self.author.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.first_name, "Jane")
        self.assertEqual(self.author.last_name, "Doe")

    def test_author_delete(self):
        response = self.client.delete(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(id=self.author.id).exists())
