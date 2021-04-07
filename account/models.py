from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.CharField(max_length=300, verbose_name='درباره نویسنده', null=True, blank=True, help_text='۳۰۰ کاراکتر')
    email = models.EmailField(unique=True, verbose_name='آدرس ایمیل', help_text='عکس پروفایل با این ایمیل از Gravatar نشان داده میشود.')
    is_author = models.BooleanField(default=False, verbose_name='کاربر نویسنده')
