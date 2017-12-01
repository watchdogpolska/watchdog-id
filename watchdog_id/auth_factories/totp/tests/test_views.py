import pyotp
from django.test import TestCase, RequestFactory
from django.urls import reverse

from watchdog_id.auth_factories.mixins import Test2FAMixin
from watchdog_id.auth_factories.totp.managers import TOTPManager
from watchdog_id.auth_factories.totp.models import OTPPassword
from watchdog_id.users.factories import UserFactory


class TestOTPPasswordCreateView(Test2FAMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('auth_factories:totp:create')
        self.factory = RequestFactory()

        super(TestOTPPasswordCreateView, self).setUp()

    def test_get_context_data(self):
        session = self.client.session

        manager = TOTPManager(session, self.user)
        secret = manager.get_totp_secret()

        session.save()

        self.assertTrue(self.login_2fa(self.user))

        response = self.client.get(self.url)
        self.assertContains(response, "data:image/png;base64")
        self.assertContains(response, secret)


class TestAuthenticationView(Test2FAMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('auth_factories:totp:index')
        self.factory = RequestFactory()

        super(TestAuthenticationView, self).setUp()

    def test_form_valid(self):
        otps = OTPPassword.objects.create(user=self.user,
                                          shared_secret="JBSWY3DPEHPK3PXP")
        totp = pyotp.TOTP("JBSWY3DPEHPK3PXP")

        self.identify_2fa(self.user)

        self.client.post(self.url, data={'token': totp.now()})

        otps.refresh_from_db()

        self.assertAlmostTimeEqual(otps.last_used, delta=5)
