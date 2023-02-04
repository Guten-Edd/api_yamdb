from http import HTTPStatus
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from rest_framework import filters, views, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (PageNumberPagination,
                                       LimitOffsetPagination)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response


from .mixins import ListCreateDeleteViewSet
from .permissions import (AdminOrSuperuserOnly, AdminOrReadOnly,
                          AuthenticatedOrReadOnly)
from .serializers import (GenreSerializer, ReviewSerializer,
                          UserSerializer, UserSignUpSerializer,
                          TokenCreateSerializer)

from reviews.models import Review, Title, Genre
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    Работа с пользователями.
    """
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticated, AdminOrSuperuserOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,)
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
        confirmation_code = get_random_string()
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
        username = User.objects.filter(username=request.data.get('username'))
        request_code = request.data.get('confirmation_code')
        confirmation_code = User.objects.filter(
            confirmation_code=request_code)
        if User.objects.filter(username=request.data.get('username'),
                               email=request.data.get('email')).exists():
            return Response(
                data={'access': str(serializer.validated_data)},
                status=HTTPStatus.OK
            )
        elif (
            username.exists() and confirmation_code != request_code
        ):
            return Response(
                data={'access': str(serializer.validated_data)},
                status=HTTPStatus.BAD_REQUEST
            )
        else:
            return Response(
                data={'access': str(serializer.validated_data)},
                status=HTTPStatus.NOT_FOUND
            )


class GenreViewSet(ListCreateDeleteViewSet):
    """
    Получить список всех жанров. Права доступа: Доступно без токена.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для отзывов.
    """
    pagination_class = PageNumberPagination
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, AuthenticatedOrReadOnly]

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
