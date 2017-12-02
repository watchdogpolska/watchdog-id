from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse

from watchdog_id.auth_factories import SESSION_KEY
from watchdog_id.auth_factories.settings import MIN_WEIGHT


def get_user_weight(user):
    if hasattr(user, 'get_auth_factory_weight'):
        return user.get_auth_factory_weight()
    return MIN_WEIGHT


def redirect_unless_full_authenticated(user_manager):
    min_weight = get_user_weight(user_manager.get_identified_user())
    if min_weight > user_manager.get_authenticated_weight():
        return redirect('auth_factories:list')
    user_manager.set_user(user_manager.get_identified_user())
    return redirect(user_manager.session.get('success_url', reverse('home')))


def get_user(request_or_session):
    from django.contrib.auth.models import AnonymousUser
    session = getattr(request_or_session, 'session', request_or_session)
    user = None
    try:
        user_id = session[SESSION_KEY]
        user = get_user_model().objects.get(pk=user_id)
    except (KeyError, get_user_model().DoesNotExist):
        pass
    return user or AnonymousUser()
