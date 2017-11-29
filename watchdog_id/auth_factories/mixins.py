from django.utils.functional import cached_property
from django.views import View

from watchdog_id.auth_factories import get_identified_user
from watchdog_id.auth_factories.shortcuts import get_user_weight


class AuthenticationProcessMixin(View):
    def get_weight(self):
        user = get_user_weight(get_identified_user(self.request))
        authenticated = self.request.user_manager.get_authenticated_weight()
        left = user - authenticated
        left = max(0, left)
        return {'user_weight': user,
                'authenticated_weight': authenticated,
                'left_weight': left}

    def get_context_data(self, **kwargs):
        kwargs.update(self.get_weight())
        return super(AuthenticationProcessMixin, self).get_context_data(**kwargs)


class SettingsViewMixin(object):

    def get_context_data(self, **kwargs):
        kwargs['factory_list'] = self.get_factory_list()
        return super(SettingsViewMixin, self).get_context_data(**kwargs)

    def get_factory_list(self):
        return [self.get_factory_item(factory) for _, factory in
                self.request.user_manager.get_available_factory_map().items()]

    @cached_property
    def enabled_factory(self):
        return self.request.user_manager.get_enabled_factory_map()

    @cached_property
    def used_factory(self):
        return self.request.user_manager.get_authenticated_factory_map()

    def get_factory_item(self, factory):
        return {'name': factory.name,
                'active': factory.id in self.enabled_factory,
                'factory': factory}
