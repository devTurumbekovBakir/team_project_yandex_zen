from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}'
