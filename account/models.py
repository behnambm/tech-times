from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.CharField(max_length=300, verbose_name='درباره نویسنده', null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name='آدرس ایمیل')
    is_author = models.BooleanField(default=False, verbose_name='کاربر نویسنده')
