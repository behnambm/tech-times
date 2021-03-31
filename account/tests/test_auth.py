from django.urls import reverse
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings


from ..models import User
from . import BaseTestCase

"""
All pre-populated data for testing are inside __init__.py.BaseTestCase.setUpTestData
"""


class LoginTestCase(BaseTestCase):
    def test_login_works_correct(self):
        logged_in = self.client.login(username='behnam', password='123')
        self.assertEqual(logged_in, True)

    def test_cant_login_with_wrong_credentials(self):
        logged_in = self.client.login(username='behnam', password='not the correct password')
        self.assertEqual(logged_in, False)

    def test_cant_access_authors_panel_without_logging_in(self):
        response = self.client.get(reverse('account:home'), follow=True)
        self.assertRedirects(response, reverse('account:login') + '?next=/account/')

    def test_redirect_to_panel_after_login(self):
        response = self.client.post(
            reverse('account:login'),
            data={'username': 'behnam', 'password': '123'},
            follow=True,
        )
        self.assertRedirects(response, reverse('account:home'))


class RegisterTestCase(BaseTestCase):
    def setUp(self):
        self.new_user_response = self.client.post(
            reverse('account:register'),
            data={
                'username': 'new_user',
                'email': 'new_user@gmail.com',
                'password1': 'SDF65478',
                'password2': 'SDF65478',
            },
            follow=True,
        )
        mail.outbox = []

    def test_register_view_and_template(self):
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')

    def test_new_user_is_inactive(self):
        user = User.objects.get(username='new_user')
        self.assertEqual(user.is_active, False)

    def test_register_new_user(self):
        response = self.client.post(
            reverse('account:register'),
            data={
                'username': 'new_user_2',
                'email': 'new_user_2@gmail.com',
                'password1': 'SDF65478',
                'password2': 'SDF65478',
            },
            follow=True,
        )
        self.assertRedirects(response, reverse('account:check_email'))
        new_user = User.objects.get(username='new_user_2')
        self.assertNotEqual(new_user, None)
        self.assertEqual(new_user.email, 'new_user_2@gmail.com')

    def test_cant_register_with_existed_username(self):
        response = self.client.post(
            reverse('account:register'),
            data={
                'username': 'new_user',
                'email': 'new_user@gmail.com',
                'password1': '123',
                'password2': '123',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('کاربری با آن نام کاربری وجود دارد', response.content.decode())

    def test_activate_new_user(self):
        user = User.objects.get(username='new_user')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        response = self.client.get(reverse('account:activate', args=(uid, token)), follow=True)

        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

        # to refresh loaded user
        user = User.objects.get(username='new_user')
        self.assertEqual(user.is_active, True)

    def test_cant_use_token_twice(self):
        user = User.objects.create_user('new_user_2', 'new_user_2@gmail.com', '123')
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # this should work fine
        response = self.client.get(reverse('account:activate', args=(uid, token)), follow=True)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

        # second request to activate user with old token. This should fail
        response = self.client.get(reverse('account:activate', args=(uid, token)), follow=True)
        self.assertIn('invalid', response.content.decode())

    def test_mail_values_are_correct(self):
        response = self.client.post(
            reverse('account:register'),
            data={
                'username': 'new_user_3',
                'email': 'new_user_3@gmail.com',
                'password1': 'SDF65478',
                'password2': 'SDF65478',
            },
            follow=True,
        )
        # to make sure register was successful
        self.assertRedirects(response, reverse('account:check_email'))

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'فعال سازی اکانت کاربری')
        self.assertIn(' با کلیک بر روی لینک زیر اکانت خود را فعال کنید.', mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].content_subtype, 'html')
        self.assertEqual(mail.outbox[0].to[0], 'new_user_3@gmail.com')

    def test_user_cant_login_without_email_confirmation(self):
        response = self.client.post(
            reverse('account:register'),
            data={
                'username': 'new_user_4',
                'email': 'new_user_4@gmail.com',
                'password1': 'SDF65478',
                'password2': 'SDF65478',
            },
            follow=True,
        )
        # to make sure register was successful
        self.assertRedirects(response, reverse('account:check_email'))

        logged_in = self.client.login(username='new_user_4', password='SDF654789')
        self.assertEqual(logged_in, False)
