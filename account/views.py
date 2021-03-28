from django.contrib.auth import views
from .forms import AccountAuthenticationForm
from django.views.generic.list import ListView
from blog.models import Article


class AccountLoginView(views.LoginView):
    form_class = AccountAuthenticationForm


class AccountView(ListView):
    model = Article
    template_name = 'account/index.html'
