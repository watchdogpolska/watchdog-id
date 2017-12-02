from unittest import TestCase

from django.test import TestCase, RequestFactory

from django.urls import reverse

from watchdog_id.auth_factories.managers import UserAuthenticationManager
from watchdog_id.auth_factories.mixins import Test2FAMixin
from watchdog_id.auth_factories.views import LoginFormView
from watchdog_id.users.factories import UserFactory


class TestFactorListView(Test2FAMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('auth_factories:list')

    def test_dispatch_unidentified_user(self):
        resp = self.client.get(self.url)
        self.assertRedirects(resp, reverse('auth_factories:login'))

    def test_dispatch_authenticated_user(self):
        self.login_2fa(self.user)
        resp = self.client.get(self.url)
        self.assertRedirects(resp, reverse('home'))


class TestLoginFormView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('auth_factories:login')
        self.factory = RequestFactory()

    def test_form_valid(self):
        request = self.factory.post(self.url, data={'user': self.user.username})
        request.session = {}

        response = LoginFormView.as_view()(request)
        self.assertEqual(response.status_code, 302)

        manager = UserAuthenticationManager(request.session)
        self.assertEqual(manager.get_identified_user(), self.user)
