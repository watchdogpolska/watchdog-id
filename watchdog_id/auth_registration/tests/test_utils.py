from django.test import TestCase
from mock import Mock

from watchdog_id.auth_registration.utils import ActivationCodeGenerator
from watchdog_id.users.factories import UserFactory


class TestActivationCodeGenerator(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_encode_and_decode_properly(self):
        generator = ActivationCodeGenerator()
        cipher = generator.encode(self.user)
        self.assertIsInstance(cipher, str)

        user = generator.decode(cipher)
        self.assertEqual(user, self.user)
