from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='نویسنده')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(unique=True, verbose_name='آدرس')
    content = RichTextUploadingField(verbose_name='محتوا')
    thumbnail = models.ImageField(upload_to='images', verbose_name='تصویر')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    status = models.CharField(choices=CHOICES, max_length=100, verbose_name='وضعیت')

    def jpublish(self):
        """This will take datetime and return in jalali format"""
        return convert_to_jalali(self.publish)

    def __str__(self):
        return self.title
