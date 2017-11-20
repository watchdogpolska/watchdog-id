
from django.shortcuts import redirect
from django.urls import reverse

from watchdog_id.auth_factories import get_authenticated_factory_list, set_user, get_identified_user
from watchdog_id.auth_factories.settings import MIN_WEIGHT


def get_authenticated_weight(request):
    return sum(factory.weight for factory in get_authenticated_factory_list(request))


def get_user_weight(user):
    if hasattr(user, 'get_auth_factory_weight'):
        return user.get_auth_factory_weight()
    return MIN_WEIGHT


def redirect_unless_full_authenticated(request):
    min_weight = get_user_weight(request.user)
    if min_weight > get_authenticated_weight(request):
        return redirect('auth_factories:list')
    set_user(request, get_identified_user(request))
    return redirect(request.session.get('success_url', reverse('home')))
