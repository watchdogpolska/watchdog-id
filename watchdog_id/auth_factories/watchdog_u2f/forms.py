import json

from atom.ext.crispy_forms.forms import SingleButtonMixin
from django import forms
from django.core import signing
from django.core.signing import SignatureExpired, BadSignature
from django.utils.translation import ugettext_lazy as _
from u2flib_server.u2f import begin_registration, complete_registration, begin_authentication, complete_authentication

from watchdog_id.auth_factories.watchdog_u2f.models import U2FToken
from watchdog_id.auth_factories.watchdog_u2f import APP_ID, FACET
from watchdog_id.auth_factories.watchdog_u2f.utils import get_user_devices


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
        return __name__ + str(self.user.pk)

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
