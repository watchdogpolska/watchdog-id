from unittest import TestCase

from django import forms

from watchdog_id.auth_factories.console_otp.forms import AuthenticationForm


class TestAuthenticationForm(TestCase):
    form_class = AuthenticationForm

    def test_valid_code_accept(self):
        data = {'password': 1234}
        form = self.form_class(data=data, code=1234)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_code_reject(self):
        data = {'password': 0000}
        form = self.form_class(data=data, code=1234)
        self.assertFalse(form.is_valid())

    def test_clean_password(self):
        data = {'password': 0000}
        form = self.form_class(data=data, code=1234)
        form.is_valid()
        with self.assertRaises(forms.ValidationError):
            form.clean_password()

    def test_verify_bypass_by_empty_password(self):
        data = {'password': ''}
        form = self.form_class(data=data, code=1234)
        self.assertFalse(form.is_valid())
