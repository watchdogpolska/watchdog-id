from django.test import TestCase

from django.contrib.auth.models import AnonymousUser, User

from watchdog_id.auth_factories.managers import UserAuthenticationManager
from watchdog_id.users.factories import UserFactory


class TestUserAuthenticationManager(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.session = self.client.session

    def test_set_or_get_or_unset_user(self):
        manager = UserAuthenticationManager(self.session)
        self.assertEqual(manager.get_user(), AnonymousUser())

        manager.set_user(self.user)
        self.assertEqual(manager.get_user(), self.user)
        self.assertEqual(manager.get_identified_user(), self.user)

        manager.unset_user()
        self.assertEqual(manager.get_user(), AnonymousUser())
        self.assertEqual(manager.get_identified_user(), None)

    def test_get_or_set_or_unset_identified_user(self):
        manager = UserAuthenticationManager(self.session)
        self.assertEqual(manager.get_user(), AnonymousUser())

        manager.set_identified_user(self.user)
        self.assertEqual(manager.get_user(), AnonymousUser())
        self.assertEqual(manager.get_identified_user(), self.user)

        manager.unset_identified_user()
        self.assertEqual(manager.get_user(), AnonymousUser())
        self.assertEqual(manager.get_identified_user(), None)

    def test_add_and_authenticated_factory(self):
        manager = UserAuthenticationManager(self.session)
        self.assertEqual(manager.get_user(), AnonymousUser())

