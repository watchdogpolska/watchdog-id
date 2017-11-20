from django.core.urlresolvers import reverse


class BaseConfig(object):
    id = None
    urlpatterns = None
    weight = 50

    @property
    def name(self):
        return self.id

    def is_available_for_user(self, factory_list):
        return True

    def get_authentication_url(self):
        return reverse('auth_factories:{}:index'.format(self.id))
