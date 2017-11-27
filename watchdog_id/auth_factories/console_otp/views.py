# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from atom.ext.crispy_forms.forms import SingleButtonMixin
from django import forms
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from watchdog_id.auth_factories import get_identified_user
from watchdog_id.auth_factories.console_otp.config import ConsoleOtpConfig
from watchdog_id.auth_factories.shortcuts import redirect_unless_full_authenticated
from watchdog_id.auth_factories.views import AuthenticationProcessMixin

SESSION_KEY_NAME = 'OTP:code'


class PasswordForm(SingleButtonMixin, forms.Form):
    password = forms.CharField(label=_("OTP"))

    error_messages = {'invalid_password': _("Please enter a correct OTP. "),
                      'lack_session_code': _("Invalid request. Lack session OTP code."),
                      }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.request = kwargs.pop('request')
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if SESSION_KEY_NAME not in self.request.session:
            raise forms.ValidationError(
                self.error_messages['lack_session_code'],
                code='lack_session_code',
            )
        if password and str(self.request.session.get(SESSION_KEY_NAME)) != password:
            raise forms.ValidationError(
                self.error_messages['invalid_password'],
                code='invalid_password',
            )

        return password


class LoginView(AuthenticationProcessMixin, FormView):
    form_class = PasswordForm
    template_name = 'password/form.html'

    def set_session_code(self):
        session_code = random.randint(1000, 9999)
        self.request.session[SESSION_KEY_NAME] = session_code
        print("The authentication code is {}.".format(session_code))

    def get(self, request, *args, **kwargs):
        self.set_session_code()
        return super(LoginView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['user'] = get_identified_user(self.request)
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _("Console OTP authentication succeeded."))
        self.request.user_manager.add_authenticated_factory(ConsoleOtpConfig)
        return redirect_unless_full_authenticated(self.request)

    def form_invalid(self, form):
        self.set_session_code()
        return super(LoginView, self).form_invalid(form)
