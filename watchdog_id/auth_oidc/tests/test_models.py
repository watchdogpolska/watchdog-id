from django.test import TestCase

from watchdog_id.auth_oidc.models import Application


class TestClientAuthentication(TestCase):
    def test_redirect_uri_for_multiple_uris(self):
        client = Application(redirect_uri_list="https://valid.com/uri\n"
                                               "https://valid.com/uri2\n"
                                               "http://localhost:5000/oidc-client-sample.html")
        self.assertTrue(client.check_redirect_uri("https://valid.com/uri"))
        self.assertTrue(client.check_redirect_uri("https://valid.com/uri2"))
        self.assertFalse(client.check_redirect_uri("https://valid.com/uri3"))
        self.assertFalse(client.check_redirect_uri("https://valid.com/"))
        self.assertFalse(client.check_redirect_uri("http://valid.com/uri"))
        self.assertFalse(client.check_redirect_uri("https://evil.com/uri"))
        self.assertTrue(client.check_redirect_uri("https://localhost:5000/oidc-client-sample.html"))
