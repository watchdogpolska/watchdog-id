from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import UpdateView


from watchdog_id.auth_factories.password.forms import PasswordForm, PasswordSettingsForm
from watchdog_id.auth_factories.password.models import PasswordSettings
from watchdog_id.auth_factories.views import BaseAuthenticationFormView
from watchdog_id.auth_factories.mixins import AuthenticationProcessMixin, SettingsViewMixin, UserFormKwargsMixin
from watchdog_id.auth_factories.password.factory import PasswordFactory


class AuthenticationView(AuthenticationProcessMixin, BaseAuthenticationFormView):
    form_class = PasswordForm
    template_name = 'password/form.html'
    success_message = _("Password authentication succeeded.")
    factory = PasswordFactory

    def get_form_kwargs(self):
        kwargs = super(AuthenticationView, self).get_form_kwargs()
        kwargs['user'] = self.user_manager.get_identified_user()
        return kwargs


class SettingsView(SettingsViewMixin, UserFormKwargsMixin, UpdateView):
    form_class = PasswordSettingsForm
    model = PasswordSettings
    success_url = reverse_lazy('auth_factories:settings')

    def get_object(self, queryset=None):
        obj, _ = PasswordSettings.objects.get_or_create(user=self.request.user)
        return obj
