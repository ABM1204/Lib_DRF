from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Author, Book, FavoriteBook
from .serializers import AuthorSerializer, BookSerializer, FavoriteBookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['authors', 'genre', 'publication_date']
    search_fields = ['title', 'authors__last_name']
    ordering_fields = ['publication_date', 'authors__last_name', 'genre']

    @extend_schema(
        parameters=[
            OpenApiParameter(name="genre", description="Filter by genre", required=False, type=str),
            OpenApiParameter(name="publication_date", description="Filter by publication date", required=False,
                             type=str),
        ],
        responses={200: BookSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)



class FavoriteBookViewSet(viewsets.ModelViewSet):
    queryset = FavoriteBook.objects.all()
    serializer_class = FavoriteBookSerializer

