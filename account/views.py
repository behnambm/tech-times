from django.contrib.auth import views
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AccountAuthenticationForm
from blog.models import Article


class AccountLoginView(views.LoginView):
    form_class = AccountAuthenticationForm


class AccountView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'account/index.html'
