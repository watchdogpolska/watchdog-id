# coding=utf-8
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from watchdog_id.auth_factories import SESSION_KEY, SESSION_IDENTIFIED_KEY, FACTORY_LIST_SESSION_KEY, Registry
from watchdog_id.auth_factories.shortcuts import get_user


class UserAuthenticationManager(object):
    def __init__(self, session):
        self.session = session

    def set_user(self, user):
        self.session[SESSION_KEY] = user.pk
        self.set_identified_user(user)

    def get_user(self):
        return get_user(self.session)

    def unset_user(self):
        if SESSION_KEY in self.session:
            del self.session[SESSION_KEY]
        self.unset_identified_user()
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
        self._identified_user = None
        if SESSION_IDENTIFIED_KEY in self.session:
            del self.session[SESSION_IDENTIFIED_KEY]
        if FACTORY_LIST_SESSION_KEY in self.session:
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
        return sum(factory.weight for factory in self.get_authenticated_factory_map().values())

    def has_any_first_factor(self):
        return any(factory.first_class for factory in self.get_authenticated_factory_map().values())

    def get_available_first_class(self):
        return [factory for factory in self.get_available_factory_map().values() if factory.first_class]
