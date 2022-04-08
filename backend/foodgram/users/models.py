from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole:
    USER = 'user'
    ADMIN = 'admin'


class CustomUser(AbstractUser):
    """Custom user model."""

    ROLES = [
        (UserRole.USER, 'user'),
        (UserRole.ADMIN, 'admin'),
    ]

    role = models.CharField(
        choices=ROLES,
        max_length=50,
        verbose_name='Роль пользователя',
        default='user',
    )
    username = models.CharField(
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        help_text='Введите адрес электронной почты',
        unique=True
    )

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    