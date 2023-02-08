from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя.
    """
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"'
            )
        return value


class UserSignUpSerializer(serializers.Serializer):
    """
    Сериализатор для регистрации нового пользователя.
    """
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(regex=r'^[\w.@+-]',
                           message='Недопустимые символы в имени пользователя')
        ]
    )
    email = serializers.CharField(
        max_length=254,
        validators=[
            EmailValidator(message='Недопустимый email')
        ]
    )

    class Meta:
        fields = '__all__'

    def create(self, value):
        return User.objects.create(**value)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"'
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Имя пользователя уже существует'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с этим адресом электронной почты уже существует'
            )
        return value


class TokenCreateSerializer(serializers.Serializer):
    """
    Сериализатор для создания токена.
    """
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=256)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Неверный код подтверждения')
        return RefreshToken.for_user(user).access_token


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для категорий.
    """

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для жанров.
    """

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для GET запросов произведений.
    """
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'rating',
                  'category', 'genre')


class TitlePostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для POST запросов произведений.
    """
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отзывов. Валидирует оценку и уникальность.
    """
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 11:
            raise serializers.ValidationError(
                'Оценка должна быть по 10-бальной шкале!'
            )
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError(
                'Только один отзыв на произведение от одного юзера!'
            )
        return data

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для комментов.
    """
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']
