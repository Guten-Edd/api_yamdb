from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Review, Title

from .mixins import ListCreateDeleteViewSet
from .serializers import CategorySerializer, GenreSerializer, ReviewSerializer


class CategoryViewSet(ListCreateDeleteViewSet):
    """
    Получить список всех категорий Права доступа: Доступно без токена.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(ListCreateDeleteViewSet):
    """
    Получить список всех жанров. Права доступа: Доступно без токена.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""
    pagination_class = PageNumberPagination
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
