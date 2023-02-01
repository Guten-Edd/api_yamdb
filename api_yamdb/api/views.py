from rest_framework.filters import SearchFilter
from reviews.models import Genre

from .mixins import ListCreateDeleteViewSet
from .serializers import GenreSerializer


class GenreViewSet(ListCreateDeleteViewSet):
    """
    Получить список всех жанров. Права доступа: Доступно без токена.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
