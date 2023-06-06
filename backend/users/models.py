from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='e-mail пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия пользователя'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('username', )
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__exact='me'),
                name="username shouldn't be 'me'"
            )
        ]

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписок."""
    subscriber = models.ForeignKey(
        User,
        related_name='subscriber',
        on_delete=models.CASCADE,
        verbose_name='пользователь, который подписывается',
    )
    subscribed = models.ForeignKey(
        User,
        related_name='subscribed',
        on_delete=models.CASCADE,
        verbose_name='пользователь, на которого подписан',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'subscribed'],
                name='shouldnt_subscribe_twice'
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F("subscribed")),
                name='shouldnt_subscribe_yourself'
            ),
        ]

    def __str__(self):
        return f' Подписка {self.subscriber} на {self.subscribed}'
