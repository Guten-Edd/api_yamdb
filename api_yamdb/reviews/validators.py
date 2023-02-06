from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """
    Валидатор проверяет что год создания произведения меньше чем нынешний год.
    """
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            f'{value} год еще не наступил.'
        )
