from django.contrib import messages
from django.shortcuts import redirect
from django.test import SimpleTestCase
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.views import View
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin

from watchdog_id.auth_factories.managers import UserAuthenticationManager
from watchdog_id.auth_factories.shortcuts import get_user_weight
from django.utils.translation import ugettext_lazy as _


class UserSessionManageMixin(View):
    def dispatch(self, request, *args, **kwargs):
        self.user_manager = UserAuthenticationManager(request.session)
        return super(UserSessionManageMixin, self).dispatch(request, *args, **kwargs)


class UserFormKwargsMixin(FormMixin):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AuthenticationProcessMixin(ContextMixin, View):
    def get_weight(self):
        user = get_user_weight(self.user_manager.get_identified_user())
        authenticated = self.user_manager.get_authenticated_weight()
        left = user - authenticated
        left = max(0, left)
        return {'user_weight': user,
                'authenticated_weight': authenticated,
                'left_weight': left}

    def dispatch(self, request, *args, **kwargs):
        self.user_manager = UserAuthenticationManager(request.session)

        if not self.user_manager.get_identified_user():
            return redirect('auth_factories:login')
        return super(AuthenticationProcessMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update(self.get_weight())
        return super(AuthenticationProcessMixin, self).get_context_data(**kwargs)


class SingleFactoryProcessMixin(AuthenticationProcessMixin):
    factory = None

    def dispatch(self, request, *args, **kwargs):
        self.user_manager = UserAuthenticationManager(request.session)
        if self.factory.id in self.user_manager.get_authenticated_factory_map():
            messages.warning(request, _("You can not use the same form of authentication twice."))
            return redirect(reverse('auth_factories:list'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['factory_name'] = self.factory().name
        kwargs['authentication_url'] = self.factory().get_authentication_url()
        return super(SingleFactoryProcessMixin, self).get_context_data(**kwargs)


class SettingsViewMixin(UserSessionManageMixin, ContextMixin, View):

    def get_context_data(self, **kwargs):
        kwargs['factory_list'] = self.get_factory_list()
        return super(SettingsViewMixin, self).get_context_data(**kwargs)

    def get_factory_list(self):
        return [self.get_factory_item(factory) for _, factory in
                self.user_manager.get_available_factory_map().items()]

    @cached_property
    def enabled_factory(self):
        return self.user_manager.get_enabled_factory_map()

    @cached_property
    def used_factory(self):
        return self.user_manager.get_authenticated_factory_map()

    def get_factory_item(self, factory):
        return {'name': factory.name,
                'active': factory.id in self.enabled_factory,
                'factory': factory}


class Test2FAMixin(SimpleTestCase):
    def login_2fa(self, user):
        session = self.client.session

        user_manager = UserAuthenticationManager(session)
        user_manager.set_user(user)

        session.save()
        return True

    def identify_2fa(self, user):
        session = self.client.session

        user_manager = UserAuthenticationManager(session)
        user_manager.set_identified_user(user)

        session.save()
        return True

    def login_2fa_factory(self, request, user):
        session = getattr(request, 'session', {})
        user_manager = UserAuthenticationManager(session)
        user_manager.set_user(user)
        request.session = session

    def identify_2fa_factory(self, request, user):
        session = getattr(request, 'session', {})
        user_manager = UserAuthenticationManager(session)
        user_manager.set_identified_user(user)
        request.session = session

    def assertAlmostTimeEqual(self, first, second=None, delta=None):
        second = second or now()
        self.assertAlmostEqual(int(first.strftime("%s")),
                               int(second.strftime("%s")),
                               delta=delta)
