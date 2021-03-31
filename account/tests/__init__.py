from django.test import TestCase
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from ..models import User
from blog.models import Article


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Test data for User model"""
        cls.behnam = User.objects.create_user(
            username='behnam',
            first_name='Behnam',
            email='behnam.mohamadzadeh21@gmail.com',
            password='123',
        )

        cls.hugo = User.objects.create_user(
            username='hugo',
            first_name='Hugo',
            email='hugoalfredha@gmail.com',
            password='123',
        )

        # to prevent sending data to Arvan Cloud
        Article.thumbnail.field.storage = FileSystemStorage()

        # Test data for Article model
        Article.objects.create(
            title='Test Article 1',
            content='Content for article 1',
            slug='article-1',
            status='published',
            author=cls.behnam,
            thumbnail=File(open('static/blog/img/home-bg.jpg', 'rb')),
        )
        Article.objects.create(
            title='Test Article 2',
            content='Content for article 2',
            slug='article-2',
            status='published',
            author=cls.behnam,
            thumbnail=File(open('static/blog/img/home-bg.jpg', 'rb')),
        )
        Article.objects.create(
            title='Test Article 3',
            content='Content for article 3',
            slug='article-3',
            status='draft',
            author=cls.behnam,
            thumbnail=File(open('static/blog/img/home-bg.jpg', 'rb')),
        )
        Article.objects.create(
            title='Test Article 4',
            content='Content for article 4',
            slug='article-4',
            status='draft',
            author=cls.hugo,
            thumbnail=File(open('static/blog/img/home-bg.jpg', 'rb')),
        )
        Article.objects.create(
            title='Test Article 5',
            content='Content for article 5',
            slug='article-5',
            status='published',
            author=cls.behnam,
            thumbnail=File(open('static/blog/img/home-bg.jpg', 'rb')),
        )
        Article.objects.create(
            title='Test Article 6',
            content='Content for article 6',
            slug='article-6',
            status='rejected',
            author=cls.behnam,
            thumbnail=File(open('static/blog/img/home-bg.jpg', 'rb')),
        )
        Article.objects.create(
            title='Test Article 7',
            content='Content for article 7',
            slug='article-7',
            status='published',
            author=cls.behnam,
            thumbnail=File(open('static/blog/img/home-bg.jpg', 'rb')),
        )
        Article.objects.create(
            title='Test Article 8',
            content='Content for article 8',
            slug='article-8',
            status='published',
            author=cls.behnam,
            thumbnail=File(open('static/blog/img/home-bg.jpg', 'rb')),
        )
        Article.objects.create(
            title='Test Article 9',
            content='Content for article 9',
            slug='article-9',
            status='pending',
            author=cls.behnam,
            thumbnail=File(open('static/blog/img/home-bg.jpg', 'rb')),
        )
        Article.objects.create(
            title='Test Article 10',
            content='Content for article 10',
            slug='article-10',
            status='published',
            author=cls.hugo,
            thumbnail=File(open('static/blog/img/home-bg.jpg', 'rb')),
        )
        Article.objects.create(
            title='Test Article 11',
            content='Content for article 11',
            slug='article-11',
            status='draft',
            author=cls.hugo,
            thumbnail=File(open('static/blog/img/home-bg.jpg', 'rb')),
        )

