from django.db import models
from django.contrib.auth.models import AbstractUser


# AbstractUser 사용
class Users(AbstractUser):
    user_auth = models.CharField(max_length=50)
    hint = models.CharField(max_length=50)