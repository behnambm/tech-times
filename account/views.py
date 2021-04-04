from django.contrib.auth import views, login
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.conf import settings
from django.urls import reverse_lazy

from .forms import AccountAuthenticationForm, UserRegistrationForm
from blog.models import Article
from .models import User
from .mixins import AuthorAccessMixin


class AccountLoginView(views.LoginView):
    form_class = AccountAuthenticationForm


class AccountView(LoginRequiredMixin, ListView):
    template_name = 'account/index.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.order_by('-created')[:10]
        return Article.objects.published().filter(author=self.request.user).order_by('-created')[:10]


class RegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = UserRegistrationForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        domain = get_current_site(self.request).domain
        msg = render_to_string(
            'registration/mail.html',
            {
                'token': default_token_generator.make_token(user),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'domain': domain,
                'protocol': 'https' if 'heroku' in domain else 'http',
            }
        )
        mail = EmailMessage(
            'فعال سازی اکانت کاربری',
            msg,
            '"Tech Times" <no-reply@techtimes.ir>',
            [user.email]
        )
        mail.content_subtype = 'html'
        mail.send()
        return redirect(reverse('account:check_email'))


def check_email(request):
    return render(request, 'registration/confirm_email.html')


def activate(request, uid, token):
    user_id = force_text(urlsafe_base64_decode(uid))
    try:
        user = User.objects.get(pk=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        raise Exception('Invalid confirmation link')
    except:
        return HttpResponse('invalid')


class CreateArticleView(AuthorAccessMixin, CreateView):
    model = Article
    template_name = 'account/create_article.html'
    success_url = reverse_lazy('account:home')

