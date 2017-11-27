from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from watchdog_id import auth_factories
from watchdog_id.auth_factories.manager import SessionFactoryManager


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth_factories.get_user(request)
    return request._cached_user


class AuthenticationMiddleware(MiddlewareMixin):
    """
        Customization of django.contrib.auth.middleware.AuthenticationMiddleware
    """

    def process_request(self, request):
        assert hasattr(request, 'session'), ("The Django authentication middleware requires session middleware "
                                             "to be installed. Edit your MIDDLEWARE%s setting to insert "
                                             "'django.contrib.sessions.middleware.SessionMiddleware' before "
                                             "'django.contrib.auth.middleware.AuthenticationMiddleware'."
                                             ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        request.user = SimpleLazyObject(lambda: get_user(request))
        request.user_manager = SessionFactoryManager(request)
