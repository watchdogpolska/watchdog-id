from abc import abstractmethod, ABCMeta

from django.core.urlresolvers import reverse

from watchdog_id.auth_factories.settings import FACTORY_SETTINGS


class BaseConfig(object):
    __metaclass__ = ABCMeta

    id = None
    urlpatterns = None
    weight = 50

    @property
    def name(self):
        return self.id

    def get_settings(self):
        return FACTORY_SETTINGS.get(self.id, {})

    def get_authentication_url(self):
        return reverse('auth_factories:{}:index'.format(self.id))

    def get_settings_url(self):
        return reverse('auth_factories:{}:settings'.format(self.id))

    def is_available(self, user):
        return True

    @abstractmethod
    def is_enabled(self, user):
        pass
