from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Review, Title

from .filters import FilterTitle
from .mixins import ListCreateDeleteViewSet
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer,
    TitlePostSerializer,
    TitleSerializer,
)


class CategoryViewSet(ListCreateDeleteViewSet):
    """
    Получить список всех категорий. Права доступа: Доступно без токена.
    Добавление новой категории. Права доступа: Администратор.
    Удаление категории. Права доступа: Администратор
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
    Добавить жанр. Права доступа: Администратор.
    Удаление жанра. Права доступа: Администратор.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получить список всех объектов. Права доступа: Доступно без токена.
    Добавление произведения. ПД: Администратор.
    Получение информации о произведении. ПД: Доступно без токена
    Частичное обновление информации о произведении.ПД: Администратор
    Удаление произведения. Права доступа: Администратор.
    """
    pagination_class = PageNumberPagination
    serializer_class = TitleSerializer
    filter_backends = (SearchFilter,)
    filterset_class = FilterTitle
    search_fields = ('name', 'year', 'genre__slug', 'category__slug')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitlePostSerializer

    def get_queryset(self):
        return Title.objects.all().annotate(rating=Avg('reviews__score'))


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
