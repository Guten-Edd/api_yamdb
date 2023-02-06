from django_filters.rest_framework import CharFilter, FilterSet
from reviews.models import Title


class FilterTitle(FilterSet):
    category = CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )
    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='iexact'
    )
    name = CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ('year', 'category', 'genre', 'name')
