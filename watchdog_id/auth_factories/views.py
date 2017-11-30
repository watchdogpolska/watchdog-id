from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
# Create your views here.
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, ListView, TemplateView

from watchdog_id.auth_factories import Registry
from watchdog_id.auth_factories.forms import LogoutForm, UserForm
from watchdog_id.auth_factories.mixins import AuthenticationProcessMixin, SettingsViewMixin, UserSessionManageMixin
from watchdog_id.auth_factories.models import Factor
from watchdog_id.auth_factories.shortcuts import redirect_unless_full_authenticated


class LoginFormView(UserSessionManageMixin, FormView):
    form_class = UserForm
    template_name = "auth_factories/login_form.html"
    success_url = reverse_lazy('auth_factories:list')

    def form_valid(self, form):
        self.request.user_manager.set_identified_user(form.cleaned_data['user'])
        return HttpResponseRedirect(self.get_success_url())


class FactorListView(AuthenticationProcessMixin, ListView):
    model = Factor

    def dispatch(self, request, *args, **kwargs):
        if self.request.user is None:
            messages.warning(self.request, _("You must first identify yourself."))
            return redirect(reverse('auth_factories:login'))
        if not self.request.user.is_anonymous():
            messages.warning(self.request, _("You do not need to authenticate more."))
            return redirect(self.request.session.get('success_url', reverse('home')))
        return super(FactorListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['factory_list'] = self.get_factory_list()
        kwargs['registry'] = Registry
        kwargs['identified_user'] = self.request.user
        return super(FactorListView, self).get_context_data(**kwargs)

    @cached_property
    def authenticated_factories(self):
        return self.request.user_manager.get_authenticated_factory_map()

    def get_factory_list(self):
        return [self.get_factory_item(x) for _, x in self.request.user_manager.get_enabled_factory_map().items()]

    def get_factory_item(self, factory):  # TODO: Move to views
        return {'name': factory.name,
                'url': factory.get_authentication_url(),
                'weight': factory.weight,
                'authenticated': factory.id in self.authenticated_factories}


class LogoutActionView(UserSessionManageMixin, FormView):
    form_class = LogoutForm
    template_name = "auth_factories/logout.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, _("The user is logged out correctly."))
        self.request.user_manager.unset_user()
        return super(LogoutActionView, self).form_valid(form)


class SettingsView(SettingsViewMixin, TemplateView):
    template_name = "auth_factories/settings.html"


class AuthenticationFormView(FormView):
    success_message = None

    def get_template_names(self):
        if getattr(self, 'template_name', None):
            return self.template_name
        return ["{}/authentication.html".format(self.factory.id),
                "auth_factories/{}/authentication.html".format(self.factory.id),
                "auth_factories/_default/authentication.html".format(self.factory.id),
                ]

    def dispatch(self, request, *args, **kwargs):
        if self.factory.id in self.request.user_manager.get_authenticated_factory_map():
            messages.warning(self.request, _("You have already used this authentication method."))
            return redirect_unless_full_authenticated(self.request)
        return super(AuthenticationFormView, self).dispatch(request, *args, **kwargs)

    @property
    def factory(self):
        raise ImproperlyConfigured('{0} is missing a factory authenticated. '
                                   'Define {0}.factory'.format(self.__class__.__name__))

    def get_succcess_message(self):
        """Get message about success authentication
        Returns:
            str: the message
        Raises:
            ImproperlyConfigured: Missing a message
        """
        if self.success_message is None:
            raise ImproperlyConfigured(
                '{0} is missing a messages about success authentication.'
                'Define {0}.succcess_message or override {0}.get_succcess_message().'
                ''.format(self.__class__.__name__))
        return self.success_message

    def get_context_data(self, **kwargs):
        kwargs['authentication_url'] = self.factory().get_authentication_url()
        kwargs['factory_name'] = self.factory().name
        return super(AuthenticationFormView, self).get_context_data(**kwargs)

    def authentication_success(self):
        messages.success(self.request, self.get_succcess_message())
        self.request.user_manager.add_authenticated_factory(self.factory)
        return redirect_unless_full_authenticated(self.request)

    def form_valid(self, form):
        return self.authentication_success()
