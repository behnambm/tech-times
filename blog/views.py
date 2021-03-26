from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404

from .models import Article
from account.models import User


class ArticleListView(ListView):
    queryset = Article.objects.published()
    paginate_by = settings.PAGINATE_COUNT


class ArticleDetailView(DetailView):

    def get_object(self, queryset=None):
        return get_object_or_404(Article.objects.published(), slug=self.kwargs.get('slug'))


class AuthorProfileView(ListView):
    paginate_by = settings.PAGINATE_COUNT
    template_name = 'account/user_detail.html'

    def get_queryset(self):
        global author
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context

