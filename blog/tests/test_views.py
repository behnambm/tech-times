from django.urls import reverse
from django.conf import settings

from . import BaseTestCase
from utils import convert_to_jalali

"""
All pre-populated data for testing are inside __init__.py.BaseTestCase.setUpTestData
"""


class ViewsTestCase(BaseTestCase):
    def setUp(self):
        self.home_url = reverse('blog:home')
        self.home_response = self.client.get(self.home_url)

        self.draft_url = reverse('blog:detail', args=('article-11',))
        self.draft_response = self.client.get(self.draft_url)

        self.published_url = reverse('blog:detail', args=('article-10',))
        self.published_response = self.client.get(self.published_url)

    def test_home_loads_properly_and_uses_right_template(self):
        self.assertEqual(self.home_response.status_code, 200)
        self.assertTemplateUsed(self.home_response, 'blog/article_list.html')

    def test_article_model_ordering(self):
        articles = self.home_response.context_data['object_list']
        self.assertEqual(articles[0].title, 'Test Article 10')

    def test_articles_publish_time_ordering(self):
        articles = self.home_response.context_data['object_list']
        self.assertLess(articles[1].publish, articles[0].publish)

    def test_home_paginate_count(self):
        self.assertEqual(len(self.home_response.context_data['object_list']), settings.PAGINATE_COUNT)

    def test_home_doesnt_have_unpublished_article(self):
        articles_title_list = [i.title for i in self.home_response.context_data['object_list']]
        self.assertNotIn('Test Article 11', articles_title_list)

    def test_cant_get_draft_article(self):
        self.assertEqual(self.draft_response.status_code, 404)

    def test_get_404_for_articles_that_doesnt_exist(self):
        response = self.client.get(reverse('blog:detail', args=('doesnt-exits',)))
        self.assertEqual(response.status_code, 404)

    def test_can_visit_articles_that_are_exist(self):
        self.assertEqual(self.published_response.status_code, 200)

    def test_author_for_article_is_correct(self):
        self.assertEqual(self.published_response.context_data['object'].author.username, 'hugo')

    def test_jalali_date_format_is_correct(self):
        j_date = self.published_response.context_data['object'].jpublish()
        date = convert_to_jalali(self.published_response.context_data['object'].publish)
        self.assertEqual(j_date, date)

    def test_article_detail_view_uses_proper_template(self):
        self.assertTemplateUsed(self.published_response, 'blog/article_detail.html')
