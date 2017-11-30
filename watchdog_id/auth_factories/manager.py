# coding=utf-8
from django.contrib.auth import get_user_model

from watchdog_id.auth_factories import SESSION_KEY, SESSION_IDENTIFIED_KEY, FACTORY_LIST_SESSION_KEY, Registry


class UserAuthenticationManager(object):
    def __init__(self, session):
        self.session = session

    def set_user(self, user):
        self.session[SESSION_KEY] = user.pk

    def unset_user(self):
        del self.session[SESSION_KEY]
        del self.session[SESSION_IDENTIFIED_KEY]
        del self.session[FACTORY_LIST_SESSION_KEY]
        self.session.flush()

    def get_identified_user(self):
        if not hasattr(self, '_identified_user'):
            try:
                user_id = self.session[SESSION_IDENTIFIED_KEY]
                self._identified_user = get_user_model().objects.get(pk=user_id)
            except (KeyError, get_user_model().DoesNotExist):
                self._identified_user = None
        return self._identified_user

    def set_identified_user(self, user):
        self.session[SESSION_IDENTIFIED_KEY] = user.pk
        self._identified_user = user

    def unset_identified_user(self):
        del self.session[SESSION_IDENTIFIED_KEY]
        del self.session[FACTORY_LIST_SESSION_KEY]

    def add_authenticated_factory(self, factory):
        current = self.session.get(FACTORY_LIST_SESSION_KEY, [])
        current.append(factory.id)
        self.session[FACTORY_LIST_SESSION_KEY] = current

    #  Shortcuts
    def get_authenticated_factory_map(self):
        return {factory_id: Registry[factory_id] for factory_id in self.session.get(FACTORY_LIST_SESSION_KEY, [])}

    def get_enabled_factory_map(self):
        return {k: v for k, v in Registry.items() if v.is_enabled(self.get_identified_user())}

    def get_active_factory_map(self):
        return {factory_id: Registry[factory_id] for factory_id in self.session.get(FACTORY_LIST_SESSION_KEY, [])}

    def get_available_factory_map(self):
        return {k: v for k, v in Registry.items() if v.is_available(self.get_identified_user())}

    def get_authenticated_weight(self):
        return sum(factory.weight for _, factory in self.get_authenticated_factory_map().items())
