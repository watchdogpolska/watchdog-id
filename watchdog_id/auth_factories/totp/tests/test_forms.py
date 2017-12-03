from unittest import TestCase

import pyotp
from django.test import TestCase
from mock import patch, MagicMock, Mock

from watchdog_id.auth_factories.totp.forms import CreateOTPPasswordForm, AuthenticationForm
from watchdog_id.auth_factories.totp.models import OTPPassword
from watchdog_id.users.factories import UserFactory

_create_form_path = 'watchdog_id.auth_factories.totp.forms.CreateOTPPasswordForm._token_validator_class'


class TestCreateOTPPasswordForm(TestCase):
    def setUp(self):
        self.user = UserFactory()

    @patch(_create_form_path, **{'return_value.verify.return_value': True})
    def test_clean_token_for_valid(self, mock):
        form = CreateOTPPasswordForm(user=self.user,
                                     totp_secret='FOO',
                                     data={'token': 1234,
                                           'device_name': "Standard"})
        self.assertTrue(form.is_valid(), form.errors)

    @patch(_create_form_path, **{'return_value.verify.return_value': False})
    def test_clean_token_for_invalid(self, mock):
        form = CreateOTPPasswordForm(user=self.user,
                                     totp_secret='FOO',
                                     data={'token': 1234,
                                           'device_name': "Standard"})
        self.assertFalse(form.is_valid())

    @patch(_create_form_path, **{'return_value.verify.return_value': True})
    def test_save(self, mock):
        form = CreateOTPPasswordForm(user=self.user,
                                     totp_secret='FOO',
                                     data={'token': 1234,
                                           'device_name': "Standard"})
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertEqual(form.instance.user, self.user)
        self.assertEqual(form.instance.shared_secret, 'FOO')


class TestAuthenticationForm(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.token = OTPPassword.objects.create(user=self.user,
                                                totp_secret='FOO')
        self.totp = pyotp.TOTP('FOO')

    def test_for_missing_token(self):
        form = AuthenticationForm(user=self.user,
                                  otp_password_list=OTPPassword.objects.all(),
                                  data={'token': 25})
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.clean_token()['totp'], None)

    def test_for_match_token(self):
        form = AuthenticationForm(user=self.user,
                                  otp_password_list=OTPPassword.objects.all(),
                                  data={'token': self.totp.now()})
        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.clean_token()['totp'], self.totp)
