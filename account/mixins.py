from django.http import Http404
from django.shortcuts import get_object_or_404

from blog.models import Article


class AuthorAccessMixin:
    """
    Handle users that are not authenticated
    Handle users that are not `author`
    Manage form fields based on user roles
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404

        if not request.user.is_author:
            raise Http404()
        self.fields = ['title', 'slug', 'content', 'thumbnail', 'publish', ]
        if request.user.is_superuser:
            self.fields += ['status', 'author']

        return super().dispatch(request, *args, **kwargs)


class AuthorDefaultFormMixin:
    """
    If user is not superuser then cannot specify the author (the user who created this article)
    Following `form_valid` method will set the logged-in user as author for new article
    """
    def form_valid(self, form):
        self.obj = form.save(commit=False)
        if not self.request.user.is_superuser and self.request.user.is_author:
            self.obj.author = self.request.user

            if self.request.resolver_match.view_name == 'account:update':
                # form.save() does not update data that is coming from `update view`
                if self.request.POST.get('status') == 'pending':
                    self.obj.status = 'pending'

            if not self.obj.status == 'pending':
                # if article is pending then skip setting default `status`
                self.obj.status = 'draft'

        return super().form_valid(form)


class UpdateAccessMixin:
    """
    Handle accessing to /update/ view to update an article
    """
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if request.user.is_superuser or (article.status in ['draft', 'rejected'] and article.author == request.user):
            return super().dispatch(request, pk, *args, **kwargs)

        raise Http404

