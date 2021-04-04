from django.http import Http404


class AuthorAccessMixin:
    def dispatch(self, request, *args, **kwargs):
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
        if self.request.user.is_author:
            self.obj.author = self.request.user

            if not self.obj.status == 'pending':
                # if article is pending then skip setting default `status`
                self.obj.status = 'draft'

        return super().form_valid(form)
