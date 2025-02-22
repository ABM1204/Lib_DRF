from celery import Celery
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
import logging

from .models import Book
from users.models import User

logger = logging.getLogger(__name__)

@shared_task
def new_books_notification():
    time = (timezone.now() - timedelta(days=1)).date()
    new_books = Book.objects.filter(publication_date__gte=time)
    if not new_books.exists():
        logger.info("No new books found.")
        return "No new books found."

    book_titles = [book.title for book in new_books]
    users_with_emails = User.objects.exclude(email="")

    for user in users_with_emails:
        send_mail(
            subject='Latest books: ',
            message='\n'.join(book_titles),
            from_email='melisovbz@gmail.com',
            recipient_list=[user.email],
        )
    logger.info(f'{new_books.count()} new books sent.')
    return f'{new_books.count()} new books sent.'


@shared_task
def anniversary_books_notification():
    now = timezone.now().date()
    anniversary_books = Book.objects.filter(
        publication_date__year__in=[now.year - 5, now.year - 10, now.year - 20]
    )
    if not anniversary_books.exists():
        logger.info("No anniversary books found.")
        return "No anniversary books found."

    book_titles = [book.title for book in anniversary_books]
    for user in User.objects.all():
        send_mail(
            subject="Anniversary books",
            message="\n".join(book_titles),
            from_email="melisovbz@gmail.com",
            recipient_list=[user.email],
        )
    logger.info(f'{anniversary_books.count()} anniversary books sent.')
    return f'{anniversary_books.count()} anniversary books sent.'
