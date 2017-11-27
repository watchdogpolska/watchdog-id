import pyotp
from atom.ext.crispy_forms.forms import SingleButtonMixin
from braces.forms import UserKwargModelFormMixin
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.totp.models import OTPPassword


class TokenField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(TokenField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """Strip spaces in middle of token"""
        value = super(TokenField, self).to_python(value)
        value.replace(' ', '')
        return value

    def run_validators(self, value):
        super(TokenField, self).run_validators(value)
        if not value.replace(' ', ' ').isdigit():
            raise ValidationError(_("Invalid token. Token consists only of digits."),
                                  code='invalid')


class CreateOTPPasswordForm(SingleButtonMixin, UserKwargModelFormMixin, forms.ModelForm):
    token = TokenField(label=_("Token"))

    def __init__(self, *args, **kwargs):
        self.totp_secret = kwargs.pop('totp_secret')
        self.totp = pyotp.TOTP(self.totp_secret)
        super(CreateOTPPasswordForm, self).__init__(*args, **kwargs)

    def clean_token(self):
        token = self.cleaned_data['token']
        if not self.totp.verify(token):
            raise forms.ValidationError(_("The token you entered is invalid. Hurry up and try again."))

    def save(self, commit=True):
        self.instance.user = self.user
        self.instance.shared_secret = self.totp_secret
        return super(CreateOTPPasswordForm, self).save(commit)

    class Meta:
        model = OTPPassword
        fields = ('device_name',)


class OTPPasswordForm(SingleButtonMixin, forms.ModelForm):
    class Meta:
        model = OTPPassword
        fields = ('device_name',)


class PasswordForm(SingleButtonMixin, forms.Form):
    token = TokenField(label=_("OTP"))

    error_messages = {'mismatch_token': _("Invalid token. No device match. Hurry up and try again."),
                      }

    def __init__(self, *args, **kwargs):
        self.totps = kwargs.pop('totps', [])
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean_token(self):
        self.print_token()
        token = self.cleaned_data.get('token')
        self.verify_token_match(token)
        return self.cleaned_data

    def verify_token_match(self, token):
        if not any(totp.verify(int(token)) for totp in self.totps):
            raise forms.ValidationError(
                self.error_messages['mismatch_token'],
                code='mismatch_token',
            )
