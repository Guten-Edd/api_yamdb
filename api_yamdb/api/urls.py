from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ReviewViewSet, GenreViewSet, UserViewSet,
                    UserSignUpViewSet, TokenCreateViewSet)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename='reviews'
)

router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)

router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', UserSignUpViewSet.as_view()),
    path('v1/auth/token/', TokenCreateViewSet.as_view()),
]
