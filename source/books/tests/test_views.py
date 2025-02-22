from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from rest_framework_simplejwt.tokens import AccessToken

from books.models import Author, Book, FavoriteBook
from rest_framework import status

User = get_user_model()


class AuthorModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name='John',
            last_name='Doe',
            biography='test biography',
            date_of_birth=date(1980, 1, 1),
            date_of_death=date(2020, 1, 1)
        )

    def test_author_str(self):
        self.assertEqual(str(self.author), "John Doe")

    def test_author_biography(self):
        self.assertEqual(self.author.biography, "test biography")

    def test_author_dates(self):
        self.assertEqual(self.author.date_of_birth, date(1980, 1, 1))
        self.assertEqual(self.author.date_of_death, date(2020, 1, 1))



class BookModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="John",
            last_name="Doe",
            biography="A famous writer.",
            date_of_birth="1980-01-01",
            date_of_death="2020-01-01"
        )
        self.book = Book.objects.create(
            title='Test Book',
            summary='Test summary',
            isbn='9876543211234',
            publication_date='2020-01-01',
            genre='Action'
        )
        self.book.authors.add(self.author)

    def test_book_str(self):
        self.assertEqual(str(self.book), "Test Book")

    def test_book_summary(self):
        self.assertEqual(self.book.summary, "Test summary")

    def test_book_isbn(self):
        self.assertEqual(self.book.isbn, "9876543211234")

    def test_book_genre(self):
        self.assertEqual(self.book.genre, "Action")

    def test_book_authors(self):
        self.assertIn(self.author, self.book.authors.all())



class FavoriteBookModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.author = Author.objects.create(
            first_name='John',
            last_name='Doe',
            biography='A famous writer.',
            date_of_birth="1980-01-01",
            date_of_death="2020-01-01"
        )
        self.book = Book.objects.create(
            title='Test Book',
            summary='Test summary',
            isbn='1237894561237',
            publication_date = "2023-01-01",
            genre = "Fantasy"
        )
        self.book.authors.add(self.author)

    def test_favorite_book_create(self):
        favorite_book = FavoriteBook.objects.create(user=self.user, book=self.book)
        self.assertEqual(favorite_book.user, self.user)
        self.assertEqual(favorite_book.book, self.book)
        self.assertEqual(str(favorite_book), f'{self.book}')

    def test_unique_together(self):
        FavoriteBook.objects.create(user=self.user, book=self.book)
        favorite_book, created = FavoriteBook.objects.get_or_create(user=self.user, book=self.book)
        self.assertFalse(created)

    def test_favorite_book_delete_book(self):
        favorite_book = FavoriteBook.objects.create(user=self.user, book=self.book)
        book_id = favorite_book.book.id
        self.book.delete()

        with self.assertRaises(FavoriteBook.DoesNotExist):
            FavoriteBook.objects.get(book_id=book_id)

    def test_favorite_book_delete_user(self):
        favorite_book = FavoriteBook.objects.create(user=self.user, book=self.book)
        user_id = favorite_book.user.id
        self.user.delete()

        with self.assertRaises(FavoriteBook.DoesNotExist):
            FavoriteBook.objects.get(user_id=user_id)

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



# class FavoriteBookViewSetTest(TestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='password')
#         self.client = APIClient()
#         token = AccessToken.for_user(self.user)
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
#
#         self.book = Book.objects.create(
#             title="test favorite book",
#             summary="favorite book",
#             isbn="1234567897415",
#             publication_date="2022-01-01",
#             genre="Action"
#         )
#
#     def test_add_favorite(self):
#         response = self.client.post('/favorite_books/add/', {'book': self.book.id})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['detail'], "Book added to favorites.")
#     def test_add_book_to_favorites_already_added(self):
#         self.client.post('/favorite_books/add/', {'book': self.book.id})
#         response = self.client.post('/favorite_books/add/', {'book': self.book.id})
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['detail'], "Book is already in your favorites.")
#
#     def test_add_nonexistent_book(self):
#         response = self.client.post('/favorite_books/add/', {'book': 99999})
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data['detail'], "Book not found.")
#
#     def test_clear_favorites(self):
#         self.client.post('/favorite_books/add/', {'book': self.book.id})
#         response = self.client.get('/favorite_books/')
#         self.assertEqual(len(response.data), 1)
#         response = self.client.post('/favorite_books/clear/', {})
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         response = self.client.get('/favorite_books/')
#         self.assertEqual(len(response.data), 0)










