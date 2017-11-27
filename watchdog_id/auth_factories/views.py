from atom.ext.crispy_forms.forms import SingleButtonMixin
from django import forms
from django.contrib import messages
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
from watchdog_id.auth_factories.shortcuts import get_user_weight
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

    def form_valid(self, form):
        self.request.user_manager.set_identified_user(form.cleaned_data['user'])
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('auth_factories:list')


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
        # if not self.request.user.is_anonymous():
        #     messages.warning(self.request, _("You do not need to authenticate more."))
        #     return redirect(self.request.session.get('success_url', reverse('home')))

        return super(FactorListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['factory_list'] = self.get_factory_list()
        kwargs['registry'] = Registry
        kwargs['identified_user'] = self.request.user
        return super(FactorListView, self).get_context_data(**kwargs)

    @cached_property
    def authenticated_list(self):
        return self.request.user_manager.get_authenticated_factory_list()

    def get_factory_list(self):
        return [self.get_factory_item(x) for x in self.request.user_manager.get_enabled_factory_list()]

    def get_factory_item(self, factory):  # TODO: Move to views
        return (factory.name, factory.get_authentication_url(), factory.weight, factory in self.authenticated_list)


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


class SettingsView(TemplateView):
    template_name = "auth_factories/settings.html"

    def get_context_data(self, **kwargs):
        kwargs['factory_list'] = self.get_factory_list()
        return super(SettingsView, self).get_context_data(**kwargs)

    def get_factory_list(self):
        return [self.get_factory_item(factory) for factory in self.request.user_manager.get_available_factory_list()]

    @cached_property
    def enabled_factory(self):
        return self.request.user_manager.get_enabled_factory_list()

    def get_factory_item(self, factory):
        print(self.enabled_factory)
        return {'name': factory.name,
                'active': factory in self.enabled_factory,
                'factory': factory}
