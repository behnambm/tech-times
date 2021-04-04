
class AuthorAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        self.fields = ['title', 'slug', 'content', 'thumbnail', 'publish', ]
        if request.user.is_superuser:
            self.fields += ['status', 'author']
        return super().dispatch(request, *args, **kwargs)
