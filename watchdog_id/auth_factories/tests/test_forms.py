from django.test import TestCase

from watchdog_id.auth_factories.forms import UserForm
from watchdog_id.users.factories import UserFactory


class TestUserForm(TestCase):
    def setUp(self):
        self.user = UserFactory(username="exist_user")

    def test_valid_user(self):
        form = UserForm(data={'user': self.user.username})
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_user(self):
        msg = 'The username you entered is not valid. The specified user does not exist.'
        form = UserForm(data={'user': "non_exist_user"})
        self.assertFalse(form.is_valid())
        self.assertIn(msg, form.errors['user'])
