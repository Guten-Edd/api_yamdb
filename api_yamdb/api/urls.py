from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
