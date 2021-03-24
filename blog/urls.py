from django.urls import path

from .views import (
    ArticleListView,
    ArticleDetailView,
    AuthorProfileView,
)

app_name = 'blog'

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('page/<int:page>/', ArticleListView.as_view(), name='home'),

    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='detail'),

    path('author/<usernmae>/', AuthorProfileView.as_view(), name='author'),
]
