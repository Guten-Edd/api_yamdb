from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


User = get_user_model()  # ЗАГЛУШКА


class Title(models.Model):
    """Модель произведение - ЗАГЛУШКА"""
    pass


class Review(models.Model):
    """Модель Ревью - отзыв, Связвна с моделью Title(самим произведением).
    Юзер может сделать только одну оценку для конкретного произведения."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    score = models.IntegerField(
        'оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique_review'
            )]

    def __str__(self):
        return self.text
