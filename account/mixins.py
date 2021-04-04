from django.http import Http404


class AuthorAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_author:
            raise Http404()
        self.fields = ['title', 'slug', 'content', 'thumbnail', 'publish', ]
        if request.user.is_superuser:
            self.fields += ['status', 'author']

        return super().dispatch(request, *args, **kwargs)
