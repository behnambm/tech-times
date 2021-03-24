from django.db import models
from django.utils import timezone

from account.models import User
from utils import convert_to_jalali


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='published')


class Article(models.Model):
    objects = ArticleManager()

    class Meta:
        ordering = ('-publish', )
    CHOICES = (
        ('published', 'منتشر شده'),
        ('draft', 'پیش نویس'),
        ('pending', 'در حال بررسی'),
        ('rejected', 'رد شده'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='images')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices=CHOICES, max_length=100)

    def jpublish(self):
        """This will take datetime and return in jalali format"""
        return convert_to_jalali(self.publish)

    def __str__(self):
        return self.title
