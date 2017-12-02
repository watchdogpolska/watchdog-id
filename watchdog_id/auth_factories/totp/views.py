from atom.views import DeleteMessageMixin
from braces.views import LoginRequiredMixin, FormValidMessageMixin, UserFormKwargsMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView

from watchdog_id.auth_factories.mixins import AuthenticationProcessMixin, SettingsViewMixin
from watchdog_id.auth_factories.totp.factory import TOTPFactory
from watchdog_id.auth_factories.totp.forms import CreateOTPPasswordForm, OTPPasswordForm, AuthenticationForm
from watchdog_id.auth_factories.totp.managers import TOTPManager
from watchdog_id.auth_factories.totp.tables import OTPPasswordTable
from watchdog_id.auth_factories.views import BaseAuthenticationFormView
from .models import OTPPassword


class UserQuerysetMixin(object):
    def get_queryset(self):
        return super(UserQuerysetMixin, self).get_queryset().filter(user=self.request.user)


class OTPPasswordListView(SettingsViewMixin, UserQuerysetMixin, SingleTableView):
    model = OTPPassword
    table_class = OTPPasswordTable


class OTPPasswordCreateView(SettingsViewMixin, LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = OTPPassword
    form_class = CreateOTPPasswordForm
    success_url = reverse_lazy('auth_factories:totp:list')
    totp_manager_class = TOTPManager

    def dispatch(self, request, *args, **kwargs):
        self.totp = self.totp_manager_class(self.request.session, self.request.user)
        return super(OTPPasswordCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(OTPPasswordCreateView, self).get_form_kwargs()
        kwargs['totp_secret'] = self.totp.get_totp_secret()
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs['totp_img'] = self.totp.get_totp_image()
        kwargs['totp_secret'] = self.totp.get_totp_secret()
        return super(OTPPasswordCreateView, self).get_context_data(**kwargs)

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class OTPPasswordUpdateView(SettingsViewMixin, LoginRequiredMixin, UserQuerysetMixin, FormValidMessageMixin,
                            UpdateView):
    model = OTPPassword
    form_class = OTPPasswordForm
    success_url = reverse_lazy('auth_factories:totp:list')

    def get_form_valid_message(self):
        return _("{0} updated!").format(self.object)


class OTPPasswordDeleteView(SettingsViewMixin, LoginRequiredMixin, DeleteMessageMixin, DeleteView):
    model = OTPPassword
    success_url = reverse_lazy('auth_factories:totp:list')

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)


class AuthenticationView(AuthenticationProcessMixin, BaseAuthenticationFormView):
    form_class = AuthenticationForm
    factory = TOTPFactory
    success_message = _("OTP authentication succeeded.")

    def get_form_kwargs(self):
        kwargs = super(AuthenticationView, self).get_form_kwargs()
        user = self.user_manager.get_identified_user()
        kwargs['otp_password_list'] = OTPPassword.objects.for_user(user).all()
        return kwargs

    def form_valid(self, form):
        form.cleaned_data['totp'].last_used = now()
        form.cleaned_data['totp'].save()
        return super(AuthenticationView, self).form_valid(form)
