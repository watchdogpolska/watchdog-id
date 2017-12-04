# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import random

from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.console_otp.factory import ConsoleOtpFactory
from watchdog_id.auth_factories.console_otp.forms import AuthenticationForm
from watchdog_id.auth_factories.views import FinishAuthenticationFormView
from watchdog_id.auth_factories.mixins import AuthenticationProcessMixin, SingleFactoryProcessMixin

SESSION_KEY_NAME = 'console_otp:code'

logger = logging.getLogger(__name__)


class CodeSessionManager(object):
    KEY = SESSION_KEY_NAME

    def __init__(self, session):
        self.session = session

    def reset_session_code(self):
        session_code = random.randint(1000, 9999)
        self.session[self.KEY] = session_code
        logger.info("The authentication code is {}.".format(session_code))

    def get_code(self):
        if self.KEY not in self.session:
            self.reset_session_code()
        return self.session[self.KEY]


class AuthenticationView(SingleFactoryProcessMixin, FinishAuthenticationFormView):
    form_class = AuthenticationForm
    template_name = 'console_otp/form.html'
    factory = ConsoleOtpFactory
    success_message = _("Console OTP authentication succeeded.")

    def dispatch(self, request, *args, **kwargs):
        self.session_manager = CodeSessionManager(request.session)
        return super(AuthenticationView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.session_manager.reset_session_code()
        return super(AuthenticationView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AuthenticationView, self).get_form_kwargs()
        kwargs['code'] = self.session_manager.get_code()
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs['code'] = self.session_manager.get_code()
        return super(AuthenticationView, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        self.session_manager.reset_session_code()
        return super(AuthenticationView, self).form_invalid(form)

    def form_valid(self, form):
        response = super(AuthenticationView, self).form_valid(form)
        self.session_manager.reset_session_code()
        return response
