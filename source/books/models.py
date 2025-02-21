from django.db import models

from users.models import User


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    biography = models.TextField()
    date_of_birth = models.DateField(blank=False, null=False)
    date_of_death = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    authors = models.ManyToManyField(Author, related_name='books')
    publication_date = models.DateField()
    genre = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.title}'


class FavoriteBook(models.Model):
    book = models.ForeignKey(Book, related_name='favorites', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.book}'