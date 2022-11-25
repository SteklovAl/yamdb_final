from api.views import UserViewSet
from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitleViewSet)

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
v1_router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
v1_router.register(
    'genres',
    GenresViewSet,
    basename='genres'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/', include(v1_router.urls)),
]
