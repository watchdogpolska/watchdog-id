from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from watchdog_id.auth_factories import SESSION_KEY
from watchdog_id.auth_factories.settings import MIN_WEIGHT
from watchdog_id.auth_factories.signals import user_authenticated


def string_concat_join(sep, values):  # TODO: Add suppor to iterators
    results = []
    for value in values[:-1]:
        results.append(value)
        results.append(sep)
    results.append(values[-1])
    return string_concat(*results)


def get_user_weight(user):
    if hasattr(user, 'get_auth_factory_weight'):
        return user.get_auth_factory_weight()
    return MIN_WEIGHT


def redirect_unless_full_authenticated(user_manager, request):
    min_weight = get_user_weight(user_manager.get_identified_user())
    if min_weight >= user_manager.get_authenticated_weight():
        return redirect('auth_factories:list')
    if not user_manager.has_any_first_factor():
        factory_list = string_concat_join(", ", [factory.name for factory in user_manager.get_available_first_class()])
        messages.warning(request, _("At least one first class factor authentication is required eg. {}.").format(factory_list))
        return redirect('auth_factories:list')
    user_authenticated.send(sender=redirect_unless_full_authenticated,
                            user=user_manager.get_identified_user(),
                            session_id=request.session._session_key,
                            request_ip=request.META.get('REMOTE_ADDR'))
    user_manager.set_user(user_manager.get_identified_user())
    return redirect(user_manager.session.get('auth_factories:login:next', reverse('home')))


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
