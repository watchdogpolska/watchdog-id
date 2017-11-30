# -*- coding: utf-8 -*-
import json

from atom.ext.crispy_forms.forms import SingleButtonMixin
from atom.views import DeleteMessageMixin
from braces.views import UserFormKwargsMixin
from django import forms
from django.core import signing
from django.core.signing import SignatureExpired, BadSignature
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django_tables2 import SingleTableView, tables, TemplateColumn
from u2flib_server.u2f import (begin_registration, begin_authentication,
                               complete_registration, complete_authentication)

from watchdog_id.auth_factories import get_identified_user
from watchdog_id.auth_factories.mixins import SettingsViewMixin, AuthenticationProcessMixin
from watchdog_id.auth_factories.views import AuthenticationFormView
from watchdog_id.auth_factories.watchdog_u2f.factory import WatchdogU2FFactory
from watchdog_id.auth_factories.watchdog_u2f.models import U2FToken

APP_ID = "https://localhost:3000"
FACET = APP_ID


def get_user_devices(user):
    return [json.loads(x.device_data) for x in user.u2f_tokens.all()]


class U2FTokenTable(tables.Table):
    action = TemplateColumn(template_name='watchdog_u2f/_u2ftoken_table.html')

    class Meta:
        model = U2FToken
        template = 'django_tables2/bootstrap-responsive.html'
        fields = ['device_name', 'last_used', 'created']


class U2FTokenForm(SingleButtonMixin, forms.ModelForm):
    class Meta:
        model = U2FToken
        fields = ['device_name', ]


class U2FTokenCreateForm(SingleButtonMixin, forms.ModelForm):
    u2f_enroll = forms.CharField(widget=forms.HiddenInput(), required=True)
    u2f_enroll_signed = forms.CharField(widget=forms.HiddenInput(), required=True)
    u2f_bind = forms.CharField(widget=forms.HiddenInput(), required=True)

    error_messages = {1: _('An unexpected error happened.'),
                      2: _('The request can not be processed because it is bad. Try reload the website.'),
                      3: _('Client configuration is not supported.'),
                      4: _('The presented device is not eligible for this request eg. already registered.'),
                      5: _('Timeout reached while waiting on device. Hurry up and try again.')}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(U2FTokenCreateForm, self).__init__(*args, **kwargs)
        self.helper.form_class = 'u2f-enroll'
        enroll = begin_registration(APP_ID, get_user_devices(self.user))
        self.fields['u2f_enroll'].initial = json.dumps(enroll)
        self.fields['u2f_enroll_signed'].initial = signing.dumps(enroll, salt=self._get_sign_salt())

    def _get_sign_salt(self):
        return self.__module__ + str(self.user.pk)

    def clean_u2f_enroll_signed(self):
        if 'u2f_enroll_signed' not in self.data:
            raise forms.ValidationError(_("Key enroll signature missing. Try again."))
        try:
            return signing.loads(self.data['u2f_enroll_signed'], max_age=5 * 60, salt=self._get_sign_salt())
        except (SignatureExpired, BadSignature):
            raise forms.ValidationError(_("Key enroll signature failed. Try again."))

    def clean_u2f_bind(self):
        if 'u2f_bind' not in self.cleaned_data:
            raise forms.ValidationError(_("Signed response missing. Try again."))
        data = json.loads(self.cleaned_data['u2f_bind'])
        if 'errorCode' in data:
            raise forms.ValidationError(self.error_messages.get(data['errorCode'],
                                                                self.error_messages[1]))
        return data

    def clean(self):
        cleaned_data = super(U2FTokenCreateForm, self).clean()
        cleaned_data['u2f_enroll_signed'] = self.clean_u2f_enroll_signed()
        cleaned_data['u2f_bind'] = self.clean_u2f_bind()
        if not self._errors:
            self.perform_binding(cleaned_data)
        return cleaned_data

    def perform_binding(self, cleaned_data):
        enroll = cleaned_data['u2f_enroll_signed']
        bind_data = cleaned_data['u2f_bind']
        try:
            cleaned_data['device'], cleaned_data['cert'] = complete_registration(enroll, bind_data, [FACET])
        except ValueError as e:
            raise forms.ValidationError("Key enrollment failed. {}.".format(str(e)))

    def save(self, commit=True):
        self.instance.user = self.user
        self.instance.device_data = json.dumps(self.cleaned_data['device'])
        return super(U2FTokenCreateForm, self).save(commit)

    class Meta:
        model = U2FToken
        fields = ['device_name', ]


class U2FTokenAuthenticationForm(SingleButtonMixin, forms.Form):
    action_text = _("Authenticate")

    u2f_challenge = forms.CharField(widget=forms.HiddenInput(), required=True)
    u2f_challenge_signed = forms.CharField(widget=forms.HiddenInput(), required=True)
    u2f_verify = forms.CharField(widget=forms.HiddenInput(), required=True)

    error_messages = {1: _('An unexpected error happened.'),
                      2: _('The request can not be processed because it is bad. Try reload the website.'),
                      3: _('Client configuration is not supported.'),
                      4: _('This device is not registered.'),
                      5: _('Timeout reached while waiting on device. Hurry up and try again.')}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(U2FTokenAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper.form_class = 'u2f-challenge'
        challenge = begin_authentication(APP_ID, get_user_devices(self.user))
        self.fields['u2f_challenge'].initial = json.dumps(challenge.data_for_client)
        self.fields['u2f_challenge_signed'].initial = signing.dumps(challenge, salt=self._get_sign_salt())

    def _get_sign_salt(self):
        return self.__module__ + str(self.user.pk)

    def clean_u2f_challenge_signed(self):
        if 'u2f_challenge_signed' not in self.data:
            raise forms.ValidationError(_("Challenge signature missing. Try again."))
        try:
            return signing.loads(self.data['u2f_challenge_signed'], max_age=5 * 60, salt=self._get_sign_salt())
        except (SignatureExpired, BadSignature):
            raise forms.ValidationError(_("Challenge signature failed"))

    def clean_u2f_verify(self):
        if 'u2f_verify' not in self.data:
            raise forms.ValidationError(_("Challenge signature missing. Try again."))
        data = json.loads(self.data['u2f_verify'])
        if 'errorCode' in data:
            raise forms.ValidationError(self.error_messages.get(data['errorCode'],
                                                                self.error_messages[1]))
        return data

    def clean(self):
        cleaned_data = super(U2FTokenAuthenticationForm, self).clean()
        cleaned_data['u2f_challenge_signed'] = self.clean_u2f_challenge_signed()
        cleaned_data['u2f_verify'] = self.clean_u2f_verify()
        if not self.errors:
            self.perform_verify(cleaned_data)
        return cleaned_data

    def perform_verify(self, cleaned_data):
        challenge = cleaned_data['u2f_challenge_signed']
        data = cleaned_data['u2f_verify']
        try:
            device, c, t = complete_authentication(challenge, data, [APP_ID])
        except ValueError as e:
            raise forms.ValidationError("Authentication failed. {}.".format(str(e)))
        cleaned_data.update({
            'keyHandle': device['keyHandle'],
            'touch': t,
            'counter': c,
            'token': self.get_token(device)
        })

    def get_token(self, device):
        return next((token for token in self.user.u2f_tokens.all()
                     if device['keyHandle'] == json.loads(token.device_data)['keyHandle']))


class UserQuerysetMixin(object):
    def get_queryset(self):
        return super(UserQuerysetMixin, self).get_queryset().filter(user=self.request.user)


class U2FTokenListView(SettingsViewMixin, UserQuerysetMixin, SingleTableView):
    model = U2FToken
    table_class = U2FTokenTable


class U2FTokenCreateView(SettingsViewMixin, UserFormKwargsMixin, CreateView):
    form = U2FTokenCreateForm
    form_class = U2FTokenCreateForm
    model = U2FToken

    def get_success_message(self):
        return _("{0} created!").format(self.object)


class U2FTokenDetailsView(SettingsViewMixin, UserQuerysetMixin, DetailView):
    model = U2FToken


class U2FTokenUpdateView(SettingsViewMixin, UserQuerysetMixin, UpdateView):
    model = U2FToken
    form_class = U2FTokenForm


class U2FTokenDeleteView(SettingsViewMixin, DeleteMessageMixin, DeleteView):
    model = U2FToken
    success_url = reverse_lazy('auth_factories:u2ftoken:list')
    form_class = U2FTokenForm


class AuthenticationView(AuthenticationProcessMixin, AuthenticationFormView):
    form_class = U2FTokenAuthenticationForm
    factory = WatchdogU2FFactory
    success_message = _("U2F authentication succeeded.")
    template_name = 'watchdog_u2f/authentication.html'

    def get_form_kwargs(self):
        kwargs = super(AuthenticationView, self).get_form_kwargs()
        kwargs['user'] = get_identified_user(self.request)
        return kwargs

    def form_valid(self, form):
        form.cleaned_data['token'].last_used = now()
        form.cleaned_data['token'].save()
        return super(AuthenticationView, self).form_valid(form)
