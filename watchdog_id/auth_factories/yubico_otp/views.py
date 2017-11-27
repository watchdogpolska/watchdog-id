# -*- coding: utf-8 -*-
from atom.views import DeleteMessageMixin
from braces.views import UserFormKwargsMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView
from django_tables2 import SingleTableView

from watchdog_id.auth_factories import get_identified_user
from watchdog_id.auth_factories.views import AuthenticationProcessMixin, AuthenticationFormView
from watchdog_id.auth_factories.yubico_otp.factory import YubicoOtpFactory
from watchdog_id.auth_factories.yubico_otp.forms import AuthenticationForm, CreateYubicoOTPDeviceForm
from watchdog_id.auth_factories.yubico_otp.models import YubicoOTPDevice
from watchdog_id.auth_factories.yubico_otp.tables import YubicoOTPDeviceTable


class UserQuerysetMixin(object):
    def get_queryset(self):
        return super(UserQuerysetMixin, self).get_queryset().filter(user=self.request.user)


class YubicoOTPDeviceListView(UserQuerysetMixin, SingleTableView):
    model = YubicoOTPDevice
    table_class = YubicoOTPDeviceTable


class YubicoOTPDeviceCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = YubicoOTPDevice
    form_class = CreateYubicoOTPDeviceForm
    success_url = reverse_lazy('auth_factories:yubico_otp:list')

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class YubicoOTPDeviceDeleteView(LoginRequiredMixin, DeleteMessageMixin, DeleteView):
    model = YubicoOTPDevice
    success_url = reverse_lazy('auth_factories:yubico_otp:list')

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)


class AuthenticationView(AuthenticationProcessMixin, AuthenticationFormView):
    form_class = AuthenticationForm
    factory = YubicoOtpFactory
    success_message = _("OTP authentication succeeded.")

    def get_form_kwargs(self):
        kwargs = super(AuthenticationView, self).get_form_kwargs()
        kwargs['user'] = get_identified_user(self.request)
        return kwargs
