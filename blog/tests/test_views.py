from django.urls import reverse
from django.conf import settings

from . import BaseTestCase

"""
All pre-populated data for testing are inside __init__.py.BaseTestCase.setUpTestData
"""


class ViewsTestCase(BaseTestCase):
    def setUp(self):
        self.home_url = reverse('blog:home')
        self.home_response = self.client.get(self.home_url)

    def test_home_loads_properly_and_uses_right_template(self):
        self.assertEqual(self.home_response.status_code, 200)
        self.assertTemplateUsed(self.home_response, 'blog/article_list.html')

    def test_article_model_ordering(self):
        articles = self.home_response.context_data['object_list']
        self.assertEqual(articles[0].title, 'Test Article 10')

    def test_home_paginate_count(self):
        self.assertEqual(len(self.home_response.context_data['object_list']), settings.PAGINATE_COUNT)

    def test_home_doesnt_have_unpublished_article(self):
        articles_title_list = [i.title for i in self.home_response.context_data['object_list']]
        self.assertNotIn('Test Article 11', articles_title_list)
