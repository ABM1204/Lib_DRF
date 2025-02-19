from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AuthorViewSet, BookViewSet, FavoriteBookViewSet

router = DefaultRouter()
router.register('authors', AuthorViewSet)
router.register('books', BookViewSet)
router.register('favoritebooks', FavoriteBookViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]