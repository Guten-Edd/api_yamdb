from api.views import GenreViewSet
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()

v1_router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(v1_router.urls)),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
