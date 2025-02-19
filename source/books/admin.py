from django.contrib import admin

from .models import Author, Book, FavoriteBook


admin.site.register(Author)
admin.site.register(Book)
admin.site.register(FavoriteBook)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'biography', 'date_of_birth', 'date_of_death')
    search_fields = ('first_name', 'last_name')
    list_filter = ('first_name', 'last_name')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'author', 'isbn', 'publication_date', 'genre')
    search_fields = ('title', 'author')
    list_filter = ('author', 'publication_date', 'genre')


class FavoriteBookAdmin(admin.ModelAdmin):
    list_display = ('author', 'book')
    search_fields = ('author', 'book')
    list_filter = ('author', 'book')


