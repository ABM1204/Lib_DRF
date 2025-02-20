from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import AuthorViewSet, BookViewSet, FavoriteBookViewSet
from users.views import UserCreateView, UserLogoutView

router = DefaultRouter()
router.register('authors', AuthorViewSet)
router.register('books', BookViewSet)
router.register('favoritebooks', FavoriteBookViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', UserCreateView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', UserLogoutView.as_view(), name='logout'),
]