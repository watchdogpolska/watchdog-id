from atom.views import ActionView
from django import forms
from atom.ext.crispy_forms.forms import SingleButtonMixin
from django.contrib import messages
from django.urls import reverse_lazy

from django.views.generic import FormView, UpdateView
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories import get_identified_user
from watchdog_id.auth_factories.password.models import PasswordSettings
from watchdog_id.auth_factories.shortcuts import redirect_unless_full_authenticated


class PasswordForm(SingleButtonMixin, forms.Form):
    password = forms.CharField(label=_("Password"))

    error_messages = {'invalid_password': _("Please enter a correct password. Note that fields may be case-sensitive.")}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.request = kwargs.pop('request')
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        password = self.cleaned_data.get('password')

        if password and not self.user.check_password(password):
            raise forms.ValidationError(
                self.error_messages['invalid_password'],
                code='invalid_password',
            )
        return self.cleaned_data


class PasswordLoginView(FormView):
    form_class = PasswordForm
    template_name = 'password/form.html'

    def get_form_kwargs(self):
        kwargs = super(PasswordLoginView, self).get_form_kwargs()
        kwargs['user'] = get_identified_user(self.request)
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        from watchdog_id.auth_factories.password.config import PasswordConfig
        messages.success(self.request, _("Password authentication succeeded."))
        self.request.user_manager.add_authenticated_factory(PasswordConfig)
        return redirect_unless_full_authenticated(self.request)


class PasswordSettingsForm(SingleButtonMixin, forms.ModelForm):
    password = forms.CharField(label=_("Password"),
                               help_text=_("Leave blank to not change password."),
                               strip=False,
                               required=False)
    retry_password = forms.CharField(label=_("Password (again)"),
                                     strip=False,
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
        fields = ('status', )


class SettingsView(UpdateView):
    form_class = PasswordSettingsForm
    model = PasswordSettings
    # form_class = PasswordSettingsForm
    success_url = reverse_lazy('auth_factories:settings')

    def get_form_kwargs(self):
        kwargs = super(SettingsView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        obj, _ = PasswordSettings.objects.get_or_create(user=self.request.user)
        return obj
