from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Review, Title
from .permissions import IsAdminOrModeratirOrAuthorOrReadOnly
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""
    permission_classes = [IsAdminOrModeratirOrAuthorOrReadOnly, ]
    pagination_class = PageNumberPagination
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
