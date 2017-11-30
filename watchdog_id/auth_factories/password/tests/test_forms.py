from unittest import TestCase

from django.test import TestCase

from django import forms

from watchdog_id.auth_factories.password.forms import PasswordForm, PasswordSettingsForm
from watchdog_id.auth_factories.password.models import PasswordSettings
from watchdog_id.users.factories import UserFactory


class TestPasswordForm(TestCase):
    def test_clean_for_valid_password(self):
        user = UserFactory(username='user', password='pass')
        form = PasswordForm(data={'password': 'pass'},
                            user=user)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid(), form.errors)
        form.clean()

    def test_clean_for_blank_password(self):
        user = UserFactory(username='user', password='pass')
        form = PasswordForm(data={'password': ''},
                            user=user)
        self.assertFalse(form.is_valid())
        with self.assertRaises(forms.ValidationError):
            form.clean()

    def test_clean_for_invalid_password(self):
        user = UserFactory(username='user', password='pass')
        form = PasswordForm(data={'password': 'WRONG'},
                            user=user)
        self.assertFalse(form.is_valid())
        with self.assertRaises(forms.ValidationError):
            form.clean()


class TestPasswordSettingsForm(TestCase):
    def test_clean_for_empty_password(self):
        user = UserFactory(username='user', password='pass')
        form = PasswordSettingsForm(data={'password': '',
                                          'retry_password': '',
                                          'status': True},
                                    user=user)
        form.is_valid()
        form.clean()

    def test_clean_for_match_password(self):
        user = UserFactory(username='user', password='pass')
        form = PasswordSettingsForm(data={'password': 'pass',
                                          'retry_password': 'pass',
                                          'status': True},
                                    user=user)
        form.is_valid()
        form.clean()

    def test_clean_for_mismatch_password(self):
        user = UserFactory(username='user', password='pass')
        form = PasswordSettingsForm(data={'password': 'pas',
                                          'retry_password': 'other_pass',
                                          'status': True},
                                    user=user)
        form.is_valid()
        with self.assertRaises(forms.ValidationError):
            form.clean()

    def test_save_for_empty_password(self):
        user = UserFactory(username='user', password='pass')
        form = PasswordSettingsForm(data={'password': '',
                                          'retry_password': '',
                                          'status': True},
                                    instance=PasswordSettings(user=user),
                                    user=user)
        form.is_valid()
        form.save()
        self.assertTrue(user.check_password('pass'))

    def test_save_for_password_provided(self):
        user = UserFactory(username='user', password='pass')
        form = PasswordSettingsForm(data={'password': 'foo',
                                          'retry_password': 'foo',
                                          'status': True},
                                    instance=PasswordSettings(user=user),
                                    user=user)
        form.is_valid()
        form.save()
        self.assertTrue(user.check_password('foo'))
