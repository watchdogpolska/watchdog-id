import pyotp
from django.test import TestCase

from watchdog_id.auth_factories.totp.managers import TOTPManager
from watchdog_id.users.factories import UserFactory


class TestTOTPManager(TestCase):
    def test_get_totp_secret(self):
        manager = TOTPManager({}, UserFactory())
        self.assertEquals(manager.get_totp_secret(), manager.get_totp_secret())

    def test_get_totp(self):
        manager = TOTPManager({}, UserFactory())
        self.assertIsInstance(manager.get_totp(), pyotp.TOTP)

    def test_get_totp_uri(self):
        user = UserFactory()
        manager = TOTPManager({}, user)
        uri = manager.get_totp_uri()
        self.assertTrue(uri.startswith("otpauth://"))
        self.assertIn(user.username, uri)

    def test_get_totp_image(self):
        manager = TOTPManager({}, UserFactory())
        self.assertTrue(manager.get_totp_image().startswith('data:image/png'))
