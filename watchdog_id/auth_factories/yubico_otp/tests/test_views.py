from django.test import TestCase

from django.test import RequestFactory
from django.urls import reverse
from mock import patch

from watchdog_id.auth_factories.mixins import Test2FAMixin
from watchdog_id.auth_factories.yubico_otp.models import YubicoOTPDevice
from watchdog_id.users.factories import UserFactory

_client_path = 'watchdog_id.auth_factories.yubico_otp.forms.OTPFieldMixin._yubico_client'

class TestAuthenticationView(Test2FAMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('auth_factories:yubico_otp:index')
        self.factory = RequestFactory()

        super(TestAuthenticationView, self).setUp()

    @patch(_client_path, **{'verify.return_value': True})
    def test_form_valid(self, mock):
        device = YubicoOTPDevice.objects.create(device_id=1234, user=self.user)
        self.assertEqual(device.last_used, None)

        self.identify_2fa(self.user)
        self.client.post(self.url, data={'otp': 1234})

        device.refresh_from_db()

        self.assertAlmostTimeEqual(device.last_used, delta=5)
