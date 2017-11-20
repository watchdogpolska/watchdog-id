from django import forms
from atom.ext.crispy_forms.forms import SingleButtonMixin
from django.shortcuts import redirect
from django.contrib import messages

from django.views.generic import FormView
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories import get_identified_user, set_user, register_authenticated_factory
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
    template_name = 'auth_factories/password/index.html'

    def get_form_kwargs(self):
        kwargs = super(PasswordLoginView, self).get_form_kwargs()
        kwargs['user'] = get_identified_user(self.request)
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        from watchdog_id.auth_factories.password.config import PasswordConfig
        messages.success(self.request, _("Password authentication succeeded."))
        register_authenticated_factory(self.request, PasswordConfig)
        return redirect_unless_full_authenticated(self.request)
