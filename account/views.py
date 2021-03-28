from django.contrib.auth import views
from .forms import AccountAuthenticationForm



class AccountLoginView(views.LoginView):
    form_class = AccountAuthenticationForm

# Create your views here.
