from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=50, verbose_name='Имя', null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=True)
    token = models.CharField(max_length=100, verbose_name='Токен верификации', null=True, blank=True)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
