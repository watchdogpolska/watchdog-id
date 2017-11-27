import base64
import cStringIO

import pyotp
import qrcode
from atom.views import DeleteMessageMixin
from braces.views import LoginRequiredMixin, FormValidMessageMixin, UserFormKwargsMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django_tables2 import SingleTableView

from watchdog_id.auth_factories import get_identified_user
from watchdog_id.auth_factories.shortcuts import redirect_unless_full_authenticated
from watchdog_id.auth_factories.totp.factory import TOTPFactory
from watchdog_id.auth_factories.totp.forms import CreateOTPPasswordForm, OTPPasswordForm, PasswordForm
from watchdog_id.auth_factories.totp.tables import OTPPasswordTable
from watchdog_id.auth_factories.views import AuthenticationProcessMixin
from .models import OTPPassword


class UserQuerysetMixin(object):
    def get_queryset(self):
        return super(UserQuerysetMixin, self).get_queryset().filter(user=self.request.user)


class OTPPasswordListView(UserQuerysetMixin, SingleTableView):
    model = OTPPassword
    table_class = OTPPasswordTable


class OTPPasswordCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = OTPPassword
    form_class = CreateOTPPasswordForm
    success_url = reverse_lazy('auth_factories:totp:list')

    def get_totp_secret(self):
        if 'totp_token' not in self.request.session:
            self.request.session['totp_token'] = pyotp.random_base32()
        return self.request.session['totp_token']

    def get_totp(self):
        if not hasattr(self, 'totp'):
            self.totp = pyotp.TOTP(self.get_totp_secret())
        return self.totp

    def get_form_kwargs(self):
        kwargs = super(OTPPasswordCreateView, self).get_form_kwargs()
        kwargs['totp_secret'] = self.get_totp_secret()
        return kwargs

    def get_totp_uri(self):
        return self.get_totp().provisioning_uri(name=self.request.user.email,
                                                issuer_name=self.request.user.email)

    def get_totp_image(self):
        image = qrcode.make(self.get_totp_uri())

        buffer = cStringIO.StringIO()
        image.save(buffer, format="JPEG")
        content = base64.b64encode(buffer.getvalue())
        return "data:image/png;base64,{}".format(content)

    def get_context_data(self, **kwargs):
        kwargs['totp_uri'] = self.get_totp_uri()
        kwargs['totp_img'] = self.get_totp_image()
        return super(OTPPasswordCreateView, self).get_context_data(**kwargs)

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class OTPPasswordUpdateView(LoginRequiredMixin, UserQuerysetMixin, FormValidMessageMixin, UpdateView):
    model = OTPPassword
    form_class = OTPPasswordForm
    success_url = reverse_lazy('auth_factories:totp:list')


    def get_form_valid_message(self):
        return _("{0} updated!").format(self.object)


class OTPPasswordDeleteView(LoginRequiredMixin, DeleteMessageMixin, DeleteView):
    model = OTPPassword
    success_url = reverse_lazy('auth_factories:totp:list')

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)


class AuthenticationView(AuthenticationProcessMixin, FormView):
    form_class = PasswordForm
    template_name = 'totp/authentication.html'

    def get_form_kwargs(self):
        kwargs = super(AuthenticationView, self).get_form_kwargs()
        user = get_identified_user(self.request)
        kwargs['totps'] = [pyotp.TOTP(x.shared_secret)
                           for x in OTPPassword.objects.for_user(user).all()]
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _("OTP authentication succeeded."))
        self.request.user_manager.add_authenticated_factory(TOTPFactory)
        return redirect_unless_full_authenticated(self.request)
