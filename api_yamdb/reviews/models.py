from django.db import models

from .validators import validate_year


class Category(models.Model):
    name = models.CharField(
        'имя категории',
        max_length=256
    )
    slug = models.SlugField(
        'слаг категории',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'название жанра',
        max_length=256
    )
    slug = models.SlugField(
        'слаг жанра',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'название',
        max_length=256
    )
    year = models.IntegerField(
        'год выпуска',
        validators=(validate_year, )
    )
    description = models.TextField(
        'описание',
        max_length=200,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name
