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


def get_identified_user(request):
    user = None
    try:
        user_id = request.session[SESSION_IDENTIFIED_KEY]
        user = get_user_model().objects.get(pk=user_id)
    except (KeyError, get_user_model().DoesNotExist):
        pass
    return user
