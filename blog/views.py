from django.conf import settings
from django.views.generic.list import ListView

from .models import Article


class ArticleListView(ListView):
    queryset = Article.objects.published()
    paginate_by = settings.PAGINATE_COUNT

