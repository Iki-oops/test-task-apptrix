from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from clients.managers import ClientManager


class Client(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'Электронная почта',
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=255,
        null=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=255,
        null=True,
    )
    sex = models.CharField(
        'Пол',
        choices=(('M', 'Мужской'), ('W', 'Женский')),
        max_length=1,
        null=True,
    )
    avatar = models.ImageField(
        'Аватар',
        upload_to='clients/avatars/images/',
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = ClientManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = 'Клиенты'
        verbose_name = 'Клиент'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_staff(self):
        return self.is_admin
