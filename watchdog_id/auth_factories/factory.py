from abc import ABCMeta, abstractmethod

from django.urls import reverse


class BaseFactory(object):
    __metaclass__ = ABCMeta

    id = None
    urlpatterns = None
    weight = 50

    @property
    def name(self):
        return self.id

    def get_authentication_url(self):
        return reverse('auth_factories:{}:index'.format(self.id))

    def get_settings_url(self):
        return reverse('auth_factories:{}:settings'.format(self.id))

    def is_available(self, user):
        return True

    @abstractmethod
    def is_enabled(self, user):
        pass
