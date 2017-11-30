from django.test import TestCase

from watchdog_id.auth_factories.password.factory import PasswordFactory
from watchdog_id.auth_factories.password.models import PasswordSettings
from watchdog_id.users.factories import UserFactory


class TestPasswordFactory(TestCase):
    def test_is_enabled(self):
        factory = PasswordFactory()
        user = UserFactory()

        # Enabled by default
        self.assertEqual(factory.is_enabled(user), True)

        # Enabled by user
        ps = PasswordSettings.objects.create(user=user, status=True)

        self.assertEqual(factory.is_enabled(user), True)

        # Disabled by user
        ps.status = False
        ps.save()

        self.assertEqual(factory.is_enabled(user), False)
