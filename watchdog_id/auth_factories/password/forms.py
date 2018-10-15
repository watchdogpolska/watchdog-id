from atom.ext.crispy_forms.forms import SingleButtonMixin
from django import forms
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.password.models import PasswordSettings


class PasswordForm(SingleButtonMixin, forms.Form):
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(),
                               )

    error_messages = {'invalid_password': _("Please enter a correct password. Note that fields may be case-sensitive.")}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError(
                self.error_messages['invalid_password'],
                code='invalid_password',
            )
        return self.cleaned_data


class PasswordSettingsForm(SingleButtonMixin, forms.ModelForm):
    password = forms.CharField(label=_("Password"),
                               help_text=_("Leave blank to not change password."),
                               widget=forms.PasswordInput(),
                               required=False)
    retry_password = forms.CharField(label=_("Password (again)"),
                                     widget=forms.PasswordInput(),
                                     required=False)
    error_messages = {'password_mismatch': _("Passwords are not identical. Passwords must match."), }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PasswordSettingsForm, self).__init__(*args, **kwargs)

    def clean(self):
        password = self.cleaned_data.get('password')
        retry_password = self.cleaned_data.get('retry_password')

        if password:
            if password != retry_password:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return self.cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        if password:
            self.user.set_password(password)
        return super(PasswordSettingsForm, self).save(commit)

    class Meta:
        model = PasswordSettings
        fields = ('status',)
