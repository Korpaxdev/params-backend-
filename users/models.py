import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.


class UserModel(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email адрес")


class PasswordResetTokenModel(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Токен")
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, verbose_name="Пользователь")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    @property
    def is_expired(self) -> bool:
        return self.created > timezone.now()

    def __str__(self):
        return f"Token={self.token}, User={self.user.username}"

    class Meta:
        verbose_name = "Токен для сброса пароля"
        verbose_name_plural = "Токены для сброса пароля"

    is_expired.fget.short_description = "Истек"
