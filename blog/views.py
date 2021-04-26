from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Article
from account.models import User


class ArticleListView(ListView):
    queryset = Article.objects.published().select_related('author')
    paginate_by = settings.PAGINATE_COUNT


class ArticleDetailView(DetailView):

    def get_object(self):
        article = get_object_or_404(Article.objects.all(), slug=self.kwargs.get('slug'))
        if self.request.user == article.author or self.request.user.is_superuser or article.status == 'published':
            return article
        raise Http404


class AuthorProfileView(ListView):
    paginate_by = settings.PAGINATE_COUNT
    template_name = 'blog/user_detail.html'

    def get_queryset(self):
        global author
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context

