from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомизация модели пользователя:
    bio - биография
    role - роль в системе
    confirmation_code - код подтверждения токена.
    """

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_USER = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(
        'E-mail',
        blank=False,
        unique=True,
        max_length=254,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        'Роль в системе',
        max_length=20,
        choices=ROLE_USER,
        default='user',
    )

    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True
    )

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'
