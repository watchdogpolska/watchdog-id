from atom.ext.crispy_forms.forms import SingleButtonMixin
from django import forms
from django.utils.translation import ugettext_lazy as _
from yubico_client.yubico_exceptions import SignatureVerificationError, StatusCodeError

from watchdog_id.auth_factories.yubico_otp.models import YubicoOTPDevice
from watchdog_id.auth_factories.yubico_otp.utils import get_client


class OTPFieldMixin(forms.Form):
    otp = forms.CharField(label=_("OTP"))

    error_messages = {'invalid_password': _("Please enter a correct OTP."),
                      'signature_mismatch': _("Token verification failed (invalid signature). Try again."),
                      'duplicate_device_id': _("The used token is already registered for the current user."),
                      'status_code': _("Token verification failed (rejected by auth server). Try again.")
                      }

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        self._validate_otp(otp)
        return otp

    def _validate_otp(self, otp):
        try:
            if otp and not get_client().verify(otp):
                raise forms.ValidationError(
                    self.error_messages['invalid_password'],
                    code='invalid_password',
                )
        except SignatureVerificationError:
            raise forms.ValidationError(
                self.error_messages['signature_mismatch'],
                code='signature_mismatch',
            )
        except StatusCodeError:
            raise forms.ValidationError(
                self.error_messages['status_code'],
                code='status_code',
            )


class AuthenticationForm(SingleButtonMixin, OTPFieldMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean_otp(self):
        otp = super(AuthenticationForm, self).clean_otp()
        self._device_user_assosiation(otp[:12])
        return otp

    def _device_user_assosiation(self, device_id):
        try:
            self.token = YubicoOTPDevice.objects.for_user(self.user).filter(device_id=device_id).get()
        except YubicoOTPDevice.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages['invalid_password'],
                code='invalid_password',
            )


class CreateYubicoOTPDeviceForm(SingleButtonMixin, OTPFieldMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CreateYubicoOTPDeviceForm, self).__init__(*args, **kwargs)

    def clean_otp(self):
        otp = super(CreateYubicoOTPDeviceForm, self).clean_otp()
        self._validate_unique_device(otp[:12])
        return otp

    def _validate_unique_device(self, device_id):
        if YubicoOTPDevice.objects.for_user(self.user).filter(device_id=device_id).exists():
            raise forms.ValidationError(
                self.error_messages['duplicate_device_id'],
                code='duplicate_device_id',
            )

    def save(self, commit=True):
        self.instance.device_id = self.cleaned_data.get('otp')[:12]
        self.instance.user = self.user
        return super(CreateYubicoOTPDeviceForm, self).save(commit)

    class Meta:
        model = YubicoOTPDevice
        fields = ('device_name', )
