from django.contrib.auth import get_user_model

Registry = {}

SESSION_KEY = '_auth_2fa_user_id'
SESSION_IDENTIFIED_KEY = '_auth_identified_user_id'
FACTORY_LIST_SESSION_KEY = '_auth_2fa_factor_list'


def get_user(request):
    from django.contrib.auth.models import AnonymousUser
    user = None
    try:
        user_id = request.session[SESSION_KEY]
        user = get_user_model().objects.get(pk=user_id)
    except (KeyError, get_user_model().DoesNotExist):
        pass
    return user or AnonymousUser()


def set_user(request, user):
    request.session[SESSION_KEY] = user.pk


def unset_user(request):
    del request.session[SESSION_KEY]
    del request.session[SESSION_IDENTIFIED_KEY]
    del request.session[FACTORY_LIST_SESSION_KEY]


def set_identified_user(request, user):
    request.session[SESSION_IDENTIFIED_KEY] = user.pk


def unset_identified_user(request):
    del request.session[SESSION_IDENTIFIED_KEY]
    del request.session[FACTORY_LIST_SESSION_KEY]


def register_authenticated_factory(request, factory):
    current = request.session.get(FACTORY_LIST_SESSION_KEY, [])
    current.append(factory.id)
    request.session[FACTORY_LIST_SESSION_KEY] = current


def get_authenticated_factory_list(request):
    return [Registry[factory_id] for factory_id in request.session.get(FACTORY_LIST_SESSION_KEY, [])]


def get_identified_user(request):
    from django.contrib.auth.models import AnonymousUser
    user = None
    try:
        user_id = request.session[SESSION_IDENTIFIED_KEY]
        user = get_user_model().objects.get(pk=user_id)
    except (KeyError, get_user_model().DoesNotExist):
        pass
    return user
