from django.contrib.auth import views, login
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.conf import settings
from django.urls import reverse_lazy
from django.db.models import Q 
from django.contrib import messages

from .forms import AccountAuthenticationForm, UserRegistrationForm
from blog.models import Article
from .models import User
from .mixins import (
    AuthorAccessMixin,
    AuthorDefaultFormMixin,
    UpdateAccessMixin,
)


class AccountLoginView(views.LoginView):
    form_class = AccountAuthenticationForm


class AccountView(LoginRequiredMixin, ListView):
    template_name = 'account/index.html'

    def get_queryset(self):
        if self.request.GET.get('q'):
            # 'q' parameter exists in GET query when user searches something
            q = self.request.GET.get('q')
            return Article.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))

        if self.request.user.is_superuser:
            return Article.objects.order_by('-created')[:10]

        return Article.objects.filter(author=self.request.user).order_by('-created')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # add searched string to template context
        if self.request.GET.get('q'):
            context['q'] = self.request.GET.get('q')
        
        return context


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
    """
    Activate user by checking information in activation link that has been sent 
    to the user's email
    """
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


class CreateArticleView(AuthorAccessMixin, AuthorDefaultFormMixin, CreateView):
    model = Article
    template_name = 'account/create_update_article.html'
    success_url = reverse_lazy('account:home')


class UpdateArticleView(AuthorAccessMixin, AuthorDefaultFormMixin, UpdateAccessMixin, UpdateView):
    model = Article
    template_name = 'account/create_update_article.html'
    success_url = reverse_lazy('account:home')


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    Show some basic information about users
    If logged-in user is superuser they can change other users information as well
    """
    template_name = 'account/profile.html'
    fields = ('username', 'first_name', 'last_name', 'email', 'bio')
    success_url = reverse_lazy('account:home')
    context_object_name = 'user_obj' # to stop causing conflict with authentication app's user object

    def get_object(self):
        if self.request.user.is_superuser:
            # some more information about user, when superuser wants to check their profile
            self.fields += ('is_author', 'is_active', 'last_login')

            username_to_edit = self.kwargs.get('username')
            if  username_to_edit and username_to_edit != self.request.user.username:
                # to make sure that the user who is being edited is not the logged-in user
                user_tor_edit = get_object_or_404(User, username=self.kwargs.get('username'))
                
                if not user_tor_edit.is_superuser:
                    return user_tor_edit
                messages.warning(self.request, 'شما اجازه ویرایش اطلاعات مدیران سایت را ندارید.')

        return User.objects.get(pk=self.request.user.pk)


class ArticleListView(ListView):
    """
    Get paginated list of all articles from logged-in user
    """
    template_name = 'account/articles_list.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_superuser:
            # If logged-in user is superuser show paginated list of all articles
            return Article.objects.all()

        elif self.request.user.is_author:
            return Article.objects.filter(author=self.request.user)

        raise Http404


class AccountPasswordChangeView(views.PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'account/article_delete.html'
    success_url = reverse_lazy('account:home')

    def dispatch(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('account:login'))
        
        article = get_object_or_404(Article, pk=pk)

        if request.user == article.author: # user wants to delete the article that owns
            return super().dispatch(request, pk, *args, **kwargs)
        
        # super user wants to delete someone else's article
        if request.user.is_superuser:
            if article.author.is_superuser:
                messages.warning(request, 'شما نمی توانید مقاله مدیران دیگر را حذف کنید.')
                return redirect(reverse('account:home'))
            else:
                return super().dispatch(request, pk, *args, **kwargs)

        messages.error(request, 'شما اجازه حذف مقاله کاربران دیگر را ندارید.', 'danger')
        return redirect(reverse('account:home'))
