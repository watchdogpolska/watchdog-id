# -*- coding: utf-8 -*-
from atom.ext.crispy_forms.forms import SingleButtonMixin
from atom.views import DeleteMessageMixin
from braces.views import UserFormKwargsMixin
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView
from django_tables2 import tables, SingleTableView, TemplateColumn

from watchdog_id.auth_factories import get_identified_user
from watchdog_id.auth_factories.views import AuthenticationProcessMixin, AuthenticationFormView
from watchdog_id.auth_factories.yubico_otp.factory import YubicoOtpFactory
from watchdog_id.auth_factories.yubico_otp.models import YubicoOTPDevice
from watchdog_id.auth_factories.yubico_otp.utils import get_client


class OTPFieldMixin(forms.Form):
    otp = forms.CharField(label=_("OTP"))

    error_messages = {'invalid_password': _("Please enter a correct OTP. ")}

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')

        if otp and not get_client().verify(otp):
            raise forms.ValidationError(
                self.error_messages['invalid_password'],
                code='invalid_password',
            )

        return otp


class AuthenticationForm(SingleButtonMixin, OTPFieldMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AuthenticationForm, self).__init__(*args, **kwargs)


class CreateYubicoOTPDeviceForm(SingleButtonMixin, OTPFieldMixin, forms.ModelForm):
    # otp = forms.CharField(label=_("OTP"))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CreateYubicoOTPDeviceForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.device_id = self.cleaned_data.get('otp')[:12]
        self.instance.user = self.user
        return super(CreateYubicoOTPDeviceForm, self).save(commit)

    class Meta:
        model = YubicoOTPDevice
        fields = ('device_name', )


class UserQuerysetMixin(object):
    def get_queryset(self):
        return super(UserQuerysetMixin, self).get_queryset().filter(user=self.request.user)


class YubicoOTPDeviceTable(tables.Table):
    action = TemplateColumn(template_name='yubico_otp/_yubicootpdevice_table.html')

    class Meta:
        model = YubicoOTPDevice
        template = 'django_tables2/bootstrap-responsive.html'
        fields = ('device_name', 'device_id', 'last_used')


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
