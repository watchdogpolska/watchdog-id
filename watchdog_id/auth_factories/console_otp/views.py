# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from watchdog_id.auth_factories.console_otp.factory import ConsoleOtpFactory
from watchdog_id.auth_factories.console_otp.forms import AuthenticationForm
from watchdog_id.auth_factories.views import AuthenticationFormView
from watchdog_id.auth_factories.mixins import AuthenticationProcessMixin

SESSION_KEY_NAME = 'OTP:code'


class LoginView(AuthenticationProcessMixin, AuthenticationFormView):
    form_class = AuthenticationForm
    template_name = 'console_otp/form.html'
    factory = ConsoleOtpFactory
    success_message = _("Console OTP authentication succeeded.")

    def reset_session_code(self):
        session_code = random.randint(1000, 9999)
        self.request.session[SESSION_KEY_NAME] = session_code
        print("The authentication code is {}.".format(session_code))

    def get(self, request, *args, **kwargs):
        self.reset_session_code()
        return super(LoginView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['code'] = self.request.session[SESSION_KEY_NAME]
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs['code'] = self.request.session[SESSION_KEY_NAME]
        return super(LoginView, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        self.reset_session_code()
        return super(LoginView, self).form_invalid(form)
