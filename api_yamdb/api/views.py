from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from reviews.models import Genre

from .serializers import GenreSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """
    Получить список всех жанров. Права доступа: Доступно без токена
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
