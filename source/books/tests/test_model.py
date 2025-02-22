from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date

from books.models import Author, Book, FavoriteBook

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












