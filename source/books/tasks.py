from celery import Celery
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail

from .models import Book
from users.models import User


@shared_task
def new_books_notification():
    time = timezone.now() - timedelta(days=1)
    new_books = Book.objects.filter(published_date__gte=time)

    for user in User.objects.all():
        book_tittles = [book.title for book in new_books]
        send_mail(
            subject='Latest books: ',
            message='\n'.join(book_tittles),
            from_email='melisovbz@gmail.com',
            recipient_list=[user.email],
        )
    return f'{new_books.count()} new books sent.'


@shared_task
def anniversary_books_notification():
    now = timezone.now().date()
    anniversary_books = Book.objects.filter(
        publication_date__year__in=[now.year - 5, now.year - 10, now.year - 20]
    )

    for user in User.objects.all():
        book_tittles = [book.title for book in anniversary_books]
        send_mail(
            subject="Anniversary books",
            message="\n".join(book_tittles),
            from_email="melisovbz@gmail.com",
            recipient_list=[user.email],
        )
    return f'{anniversary_books.count()} anniversary books sent.'
