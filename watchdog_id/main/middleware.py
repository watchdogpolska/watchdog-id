import re

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class FakeSSLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.is_secure = lambda: True
        request.environ['wsgi.url_scheme'] = 'https'

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
