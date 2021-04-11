from django.contrib import admin

from .models import Article

admin.site.site_header = 'مدیریت تِک تایمز'
admin.site.register(Article)
