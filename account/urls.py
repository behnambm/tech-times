from django.contrib.auth import views
from django.urls import path

from .views import (
    AccountView,
    AccountLoginView,
    RegistrationView,
    activate,
    check_email,
)

app_name = 'account'
urlpatterns = [
    path('', AccountView.as_view(), name='home'),

    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uid>/<token>/', activate, name='activate'),
    path('register/check/', check_email, name='check_email'),
    # path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #
    # path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
