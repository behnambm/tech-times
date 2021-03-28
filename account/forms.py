from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.utils.translation import gettext, gettext_lazy as _


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