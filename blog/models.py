from django.db import models
from django.utils import timezone


class Article(models.Model):
    CHOICES = (
        ('published', 'منتشر شده'),
        ('draft', 'پیش نویس'),
        ('pending', 'در حال بررسی'),
        ('rejected', 'رد شده'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='images')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices=CHOICES, max_length=100)
