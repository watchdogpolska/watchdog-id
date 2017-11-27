from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, UpdateView

from watchdog_id.auth_factories import get_identified_user
from watchdog_id.auth_factories.password.forms import PasswordForm, PasswordSettingsForm
from watchdog_id.auth_factories.password.models import PasswordSettings
from watchdog_id.auth_factories.shortcuts import redirect_unless_full_authenticated
from watchdog_id.auth_factories.views import AuthenticationProcessMixin


class AuthenticationView(AuthenticationProcessMixin, FormView):
    form_class = PasswordForm
    template_name = 'password/form.html'

    def get_form_kwargs(self):
        kwargs = super(AuthenticationView, self).get_form_kwargs()
        kwargs['user'] = get_identified_user(self.request)
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        from watchdog_id.auth_factories.password.config import PasswordFactory
        messages.success(self.request, _("Password authentication succeeded."))
        self.request.user_manager.add_authenticated_factory(PasswordFactory)
        return redirect_unless_full_authenticated(self.request)


class SettingsView(UpdateView):
    form_class = PasswordSettingsForm
    model = PasswordSettings
    success_url = reverse_lazy('auth_factories:settings')

    def get_form_kwargs(self):
        kwargs = super(SettingsView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        obj, _ = PasswordSettings.objects.get_or_create(user=self.request.user)
        return obj
