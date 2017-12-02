from unittest import TestCase

from django.test import TestCase
from mock import patch
from yubico_client.yubico_exceptions import SignatureVerificationError, StatusCodeError

from watchdog_id.auth_factories.yubico_otp.forms import AuthenticationForm, CreateYubicoOTPDeviceForm
from watchdog_id.auth_factories.yubico_otp.models import YubicoOTPDevice
from watchdog_id.users.factories import UserFactory

_client_path = 'watchdog_id.auth_factories.yubico_otp.forms.OTPFieldMixin._yubico_client'


class TestAuthenticationForm(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_clean_otp_for_valid_token(self):
        YubicoOTPDevice.objects.create(device_id=1234, user=self.user)

        with patch(_client_path, **{'verify.return_value': True}):
            form = AuthenticationForm(user=self.user,
                                      data={'otp': 1234})
            self.assertTrue(form.is_valid(), form.errors)

    def test_clean_otp_for_different_invalid_token(self):
        YubicoOTPDevice.objects.create(device_id=1234, user=self.user)

        with patch(_client_path, **{'verify.side_effect': SignatureVerificationError("X", "Y")}):
            form = AuthenticationForm(user=self.user,
                                      data={'otp': 1234})
            self.assertFalse(form.is_valid())

        with patch(_client_path, **{'verify.side_effect': StatusCodeError(500)}):
            form = AuthenticationForm(user=self.user,
                                      data={'otp': 1234})
            self.assertFalse(form.is_valid())

    def test_missing_device(self):
        with patch(_client_path, **{'verify.return_value': True}):
            form = AuthenticationForm(user=self.user,
                                      data={'otp': 1234})
            self.assertFalse(form.is_valid(), form.errors)


class TestCreateYubicoOTPDeviceForm(TestCase):
    def setUp(self):
        self.user = UserFactory()

    @patch(_client_path, **{'verify.return_value': True})
    def test_clean_otp_for_unique_device(self, mock):
        form = CreateYubicoOTPDeviceForm(user=self.user,
                                         data={'otp': 1234,
                                               'device_name': 'Lorem'})
        self.assertTrue(form.is_valid(), form.errors)
        form.save()

    @patch(_client_path, **{'verify.return_value': True})
    def test_clean_otp_for_duplicate_device(self, mock):
        YubicoOTPDevice.objects.create(device_id=1234, user=self.user)

        form = CreateYubicoOTPDeviceForm(user=self.user,
                                         data={'otp': 1234,
                                               'device_name': 'Lorem'})
        self.assertFalse(form.is_valid())
