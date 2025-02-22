from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from rest_framework_simplejwt.tokens import AccessToken

from .models import Author, Book
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


class BookViewSetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.author = Author.objects.create(first_name="John",
                                            last_name="Smith",
                                            date_of_birth="1980-01-01")
        self.book = Book.objects.create(
            title="Chainsaw Man",
            summary="A manga about a demon hunter",
            isbn="978-1234567890",
            publication_date="2021-12-03",
            genre="Action"
        )
        self.book.authors.set([self.author])

    def test_book_list(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_book_detail(self):
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Chainsaw Man")

    def test_book_create(self):
        data = {
            "title": "New Book",
            "summary": "A summary of a new book.",
            "isbn": "1234567899637",
            "authors": [self.author.id],
            "publication_date": "2023-01-01",
            "genre": "Fantasy"
        }
        response = self.client.post('/api/books/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Book")

    def test_book_update(self):
        updated_data = {
            "title": "Updated Chainsaw Man",
            "summary": "Updated summary of Chainsaw Man",
            "isbn": "1234567899635",
            "authors": [self.author.id],
            "publication_date": "2022-01-01",
            "genre": "Action"
        }
        response = self.client.put(f'/api/books/{self.book.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Chainsaw Man")
        self.assertEqual(self.book.summary, "Updated summary of Chainsaw Man")

    def test_book_delete(self):
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())