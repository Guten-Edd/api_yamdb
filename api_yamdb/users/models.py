from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    ROLE = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(regex=r'^[\w.@+-]',
                           message='Недопустимые символы в имени пользователя')
        ]
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Об авторе',
        blank=True
    )
    role = models.TextField(
        'Роль',
        choices=ROLE,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=255,
        blank=True,
        null=True
    )
    password = models.CharField(
        'Пароль',
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-date_joined']

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def __str__(self):
        return self.username
