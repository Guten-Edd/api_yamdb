from http import HTTPStatus

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, views, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .filters import FilterTitle
from .mixins import ListCreateDeleteViewSet
from .permissions import (
    AdminOrReadOnly,
    AdminOrSuperUserOnly,
    AuthenticatedOrReadOnly
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitlePostSerializer,
    TitleSerializer,
    TokenCreateSerializer,
    UserSerializer,
    UserSignUpSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    Работа с пользователями.
    """
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticated, AdminOrSuperUserOnly, )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('role'):
            serializer.validated_data.pop('role')
        serializer.save()
        return Response(serializer.data)


class UserSignUpViewSet(views.APIView):
    """
    Регистрация нового пользователя. Получение кода подтверждения.
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        if User.objects.filter(username=request.data.get('username'),
                               email=request.data.get('email')).exists():
            return Response(request.data, status=HTTPStatus.OK)
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = get_random_string(length=256)
        serializer.save(confirmation_code=confirmation_code)
        send_mail(
            'Confirmation code for Yamdb',
            f'Your confirmation code {confirmation_code}',
            'admin@yamdb.com',
            [serializer.validated_data['email']],
        )
        return Response(
            data=serializer.validated_data,
            status=HTTPStatus.OK
        )


class TokenCreateViewSet(views.APIView):
    """
    Выдача токена авторизации.
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            data={'access': str(serializer.validated_data)},
            status=HTTPStatus.OK
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
    permission_classes = (AdminOrReadOnly, )


class GenreViewSet(ListCreateDeleteViewSet):
    """
    Получить список всех жанров. Права доступа: Доступно без токена.
    Добавить жанр. Права доступа: Администратор.
    Удаление жанра. Права доступа: Администратор.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly, )
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
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterTitle
    search_fields = ('name', 'year', 'genre__slug', 'category__slug')
    permission_classes = (AdminOrReadOnly, )
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitlePostSerializer

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('reviews__score')).order_by('name')


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для отзывов.
    """
    pagination_class = PageNumberPagination
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, AuthenticatedOrReadOnly, )

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для комментариев.
    """
    serializer_class = CommentSerializer
    permission_classes = (AuthenticatedOrReadOnly, )

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return Comment.objects.filter(review=self.get_review().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
