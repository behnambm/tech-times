from . import BaseTestCase

from ..models import Article
from account.models import User


class ModelsTestCase(BaseTestCase):
    def test_article_user_models_connected(self):
        behnam = User.objects.get(username='behnam')
        article1 = Article.objects.get(slug='article-1')
        self.assertEqual(article1.author, behnam)
