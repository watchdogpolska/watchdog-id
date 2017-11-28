from atom.ext.crispy_forms.forms import SingleButtonMixin
from django import forms
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
# Create your views here.
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import FormView, ListView, TemplateView

from watchdog_id.auth_factories import Registry, get_identified_user
from watchdog_id.auth_factories.models import Factor
from watchdog_id.auth_factories.shortcuts import get_user_weight, redirect_unless_full_authenticated
from watchdog_id.users.models import User


class UserForm(SingleButtonMixin, forms.Form):
    action_text = _("Log in")
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  to_field_name='username',
                                  widget=forms.widgets.TextInput(),
                                  empty_label=None,
                                  label=_("Username"))


class LoginFormView(FormView):
    form_class = UserForm
    template_name = "auth_factories/login_form.html"
    success_url = reverse_lazy('auth_factories:list')

    def form_valid(self, form):
        self.request.user_manager.set_identified_user(form.cleaned_data['user'])
        return HttpResponseRedirect(self.get_success_url())


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


class LogoutForm(SingleButtonMixin, forms.Form):
    action_text = _("Log out")


class LogoutActionView(FormView):
    form_class = LogoutForm
    template_name = "auth_factories/logout.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, _("The user is logged out correctly."))
        self.request.user_manager.unset_user()
        return super(LogoutActionView, self).form_valid(form)


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
