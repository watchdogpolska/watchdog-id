from django.test import TestCase, RequestFactory
from django.urls import reverse

from watchdog_id.auth_factories.console_otp.views import AuthenticationView, CodeSessionManager
from watchdog_id.auth_factories.manager import UserAuthenticationManager
from watchdog_id.users.factories import UserFactory


class TestAuthenticationView(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.factory = RequestFactory()
        self.url = reverse('auth_factories:console_otp:index')
        super(TestAuthenticationView, self).setUp()

    def test_status_for_get_without_identified_user(self):
        request = self.factory.get(self.url)
        request.session = {}
        request.user_manager = UserAuthenticationManager(request.session)
        response = AuthenticationView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_status_for_get_with_identified_user(self):
        request = self.factory.get(self.url)
        request.session = {}
        request.user_manager = UserAuthenticationManager(request.session)
        request.user_manager.set_identified_user(self.user)
        response = AuthenticationView.as_view()(request)
        self.assertEquals(response.status_code, 200)

    def test_status_for_post_with_skip_get(self):
        request = self.factory.post(self.url)
        request.session = {}
        request.user_manager = UserAuthenticationManager(request.session)
        request.user_manager.set_identified_user(self.user)
        response = AuthenticationView.as_view()(request)
        self.assertEquals(response.status_code, 200)

    def test_form_invalid(self):
        session = {}

        request = self.factory.post(self.url, data={'password': 1234})

        user_manager = UserAuthenticationManager(session)
        user_manager.set_identified_user(self.user)

        request.session = session
        request.user_manager = user_manager

        response = AuthenticationView.as_view()(request)
        self.assertContains(response, "Please enter a correct OTP.")

    def test_form_valid(self):
        session = self.client.session

        user_manager = UserAuthenticationManager(session)
        user_manager.set_identified_user(self.user)

        code_manager = CodeSessionManager(session)
        code = code_manager.get_code()

        session.save()

        response = self.client.post(self.url, data={'password': code})

        self.assertRedirects(response, reverse('auth_factories:list'))
