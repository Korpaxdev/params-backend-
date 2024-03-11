from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class UserModel(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email адрес")
