from django import forms
from atom.ext.crispy_forms.forms import SingleButtonMixin
from django.shortcuts import redirect
from django.contrib import messages

from django.views.generic import FormView
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories import get_identified_user, set_user


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
        set_user(self.request, form.user)
        messages.success(self.request, _("Password authentication succeeded."))
        return redirect('auth_factories:list')
