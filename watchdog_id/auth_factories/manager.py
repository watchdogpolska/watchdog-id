from django.contrib.auth import logout

from watchdog_id.auth_factories import SESSION_KEY, SESSION_IDENTIFIED_KEY, FACTORY_LIST_SESSION_KEY, Registry, \
    get_identified_user


class SessionFactoryManager(object):
    def __init__(self, request):
        self.request = request

    def set_user(self, user):
        self.request.session[SESSION_KEY] = user.pk

    def unset_user(self):
        del self.request.session[SESSION_KEY]
        del self.request.session[SESSION_IDENTIFIED_KEY]
        del self.request.session[FACTORY_LIST_SESSION_KEY]
        logout(self.request)

    def set_identified_user(self, user):
        self.request.session[SESSION_IDENTIFIED_KEY] = user.pk

    def unset_identified_user(self):
        del self.request.session[SESSION_IDENTIFIED_KEY]
        del self.request.session[FACTORY_LIST_SESSION_KEY]

    def add_authenticated_factory(self, factory):
        current = self.request.session.get(FACTORY_LIST_SESSION_KEY, [])
        current.append(factory.id)
        self.request.session[FACTORY_LIST_SESSION_KEY] = current

    def get_authenticated_factory_map(self):
        return {factory_id: Registry[factory_id] for factory_id in self.request.session.get(FACTORY_LIST_SESSION_KEY, [])}

    def get_enabled_factory_map(self):
        return {k: v for k, v in Registry.items() if v.is_enabled(get_identified_user(self.request))}

    def get_active_factory_map(self):
        return {factory_id: Registry[factory_id] for factory_id in self.request.session.get(FACTORY_LIST_SESSION_KEY, [])}

    def get_available_factory_map(self):
        return {k: v for k, v in Registry.items() if v.is_available(self.request.user)}

    def get_authenticated_weight(self):
        return sum(factory.weight for _, factory in self.get_authenticated_factory_map().items())
