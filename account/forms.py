from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from .models import User


class AccountAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'placeholder': 'نام کاربری',
            }
        )
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'placeholder': 'رمزعبور',
            }
        ),
    )


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'placeholder': 'نام کاربری'})
        self.fields['email'].widget.attrs.update({'placeholder': 'ایمیل'})
        self.fields['email'].required = True
        self.fields['password1'].widget.attrs.update({'placeholder': 'رمزعبور'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'تکرار رمزعبور'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
