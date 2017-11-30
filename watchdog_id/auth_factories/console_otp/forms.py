from atom.ext.crispy_forms.forms import SingleButtonMixin
from django import forms
from django.utils.translation import ugettext_lazy as _


class AuthenticationForm(SingleButtonMixin, forms.Form):
    password = forms.CharField(label=_("OTP"))

    error_messages = {'invalid_password': _("Please enter a correct OTP. ")}

    def __init__(self, *args, **kwargs):
        self.code = kwargs.pop('code')
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not password or str(self.code) != password:
            raise forms.ValidationError(
                self.error_messages['invalid_password'],
                code='invalid_password',
            )

        return password
