from datetime import date

from rest_framework.exceptions import ValidationError


def validate_year(value):
    creation_year = int(date.today().year)
    if value > creation_year or value <= 0:
        raise ValidationError('Недопустимый год выпуска!')
