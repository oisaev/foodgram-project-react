from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='E-mail пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__exact='me'),
                name="username shouldn't be 'me'"
            )
        ]

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriber',
        on_delete=models.CASCADE,
        verbose_name='Пользователь, который подписывается',
    )
    subscribed_to = models.ForeignKey(
        User,
        related_name='subscribed',
        on_delete=models.CASCADE,
        verbose_name='Пользователь, на которого подписан',
    )
