from django.contrib.auth import views
from django.urls import path

from .views import (
    AccountView,
    AccountLoginView,
    RegistrationView,
    activate,
    check_email,
    CreateArticleView,
    UpdateArticleView,
    ProfileView,
    ArticleListView,
    AccountPasswordChangeView,
    ArticleDeleteView,
)

app_name = 'account'
urlpatterns = [
    path('', AccountView.as_view(), name='home'),
    path('create/', CreateArticleView.as_view(), name='create'),
    path('update/<pk>/', UpdateArticleView.as_view(), name='update'),
    path('delete/<int:pk>/', ArticleDeleteView.as_view(), name='delete'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<username>/', ProfileView.as_view(), name='profile'),
    path('list/', ArticleListView.as_view(), name='list'),
    path('list/page/<int:page>/', ArticleListView.as_view(), name='list'),

    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uid>/<token>/', activate, name='activate'),
    path('register/check/', check_email, name='check_email'),
    path('password_change/', AccountPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
