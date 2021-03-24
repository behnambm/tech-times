from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404

from .models import Article


class ArticleListView(ListView):
    queryset = Article.objects.published()
    paginate_by = settings.PAGINATE_COUNT


class ArticleDetailView(DetailView):

    def get_object(self, queryset=None):
        return get_object_or_404(Article.objects.published(), slug=self.kwargs.get('slug'))


class AuthorProfileView(DetailView):
    pass
