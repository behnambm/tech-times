from django.conf import settings
from django.views.generic.list import ListView

from .models import Article


class ArticleListView(ListView):
    model = Article
    paginate_by = settings.PAGINATE_COUNT

