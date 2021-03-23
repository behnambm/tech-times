from django.urls import path

from .views import ArticleListView

app_name = 'blog'

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('page/<int:page>/', ArticleListView.as_view(), name='home'),
]