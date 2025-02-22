from django.test import TestCase
from django.core import mail
from django.utils import timezone
from datetime import timedelta
from books.models import Book
from users.models import User
from books.tasks import new_books_notification, anniversary_books_notification


class NewBooksNotificationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password"
        )
        self.old_book = Book.objects.create(
            title="Old Book",
            summary='Test summary',
            isbn='9876543211234',
            publication_date=(timezone.now() - timedelta(days=2)).date(),
            genre='Action'
        )
        self.new_book = Book.objects.create(
            title="New Book",
            summary='Test summary',
            isbn='9876543211235',
            publication_date=(timezone.now() - timedelta(hours=12)).date(),
            genre='Action'
        )
        self.user.save()

    def test_new_books_notification(self):
        new_books_notification()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Latest books: ")
        self.assertIn("New Book", mail.outbox[0].body)
        self.assertNotIn("Old Book", mail.outbox[0].body)



class AnniversaryBooksNotificationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password"
        )
        self.anniversary_book_10_years = Book.objects.create(
            title="Anniversary Book 10 Years",
            summary='Test summary',
            isbn='9876543211236',
            publication_date=(timezone.now() - timedelta(days=3650)).date(),
            genre='Action'
        )
        self.anniversary_book_5_years = Book.objects.create(
            title="Anniversary Book 5 Years",
            summary='Test summary',
            isbn='9876543211237',
            publication_date=(timezone.now() - timedelta(days=1825)).date(),
            genre='Action'
        )
        self.anniversary_book_20_years = Book.objects.create(
            title="Anniversary Book 20 Years",
            summary='Test summary',
            isbn='9876543211238',
            publication_date=(timezone.now() - timedelta(days=7300)).date(),
            genre='Action'
        )

    def test_anniversary_books_notification(self):
        anniversary_books_notification()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Anniversary books")
        self.assertIn("Anniversary Book 10 Years", mail.outbox[0].body)
        self.assertIn("Anniversary Book 5 Years", mail.outbox[0].body)
        self.assertIn("Anniversary Book 20 Years", mail.outbox[0].body)