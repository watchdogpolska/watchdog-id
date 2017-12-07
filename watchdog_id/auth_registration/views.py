from atom.ext.crispy_forms.forms import SingleButtonMixin
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import get_password_validators
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import RedirectView

from watchdog_id.auth_registration.models import Activation
from watchdog_id.auth_registration.utils import ActivationCodeGenerator
from watchdog_id.users.models import User


class UserRegistrationForm(SingleButtonMixin, forms.ModelForm):
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(),
                               strip=False)
    retry_password = forms.CharField(label=_("Password (again)"),
                                     widget=forms.PasswordInput(),
                                     strip=False)

    error_messages = {'password_mismatch': _("Passwords are not identical. Passwords must match."),
                      'username_taken': _("This username is currently used. You can not use it again.")}

    action_text = _("Create account")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text = _("It will be used to send an activation link for the account.")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                self.error_messages['username_taken'],
                code='username_taken',
            )
        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        retry_password = self.cleaned_data.get('retry_password')

        if password != retry_password:
            self.add_error('retry_password', forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            ))
        password_validation.validate_password(password, self.instance)
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email']


class RegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    model = User
    success_message = _("The user account has been created. An e-mail with an activation link has been sent. "
                        "Click it to activate your account.")
    template_name_suffix = "_registration"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_activation_mail(form.instance)
        return response

    def send_activation_mail(self, user):
        context = self.get_activation_mail_context(user)
        user.email_user(subject=_("Account activation"),
                        message=self.get_recovery_mail_txt(context),
                        html_message=self.get_recovery_mail_html(context))

    def get_activation_mail_context(self, user):
        activation_code = ActivationCodeGenerator().encode(user)
        url = reverse('auth_registration:confirmation',
                      kwargs={'code': activation_code})
        url = self.request.build_absolute_uri(url)
        return {'user': user,
                'code': activation_code,
                'site': get_current_site(self.request),
                'url': url}

    def get_recovery_mail_txt(self, context):
        return render_to_string('auth_registration/_activation_mail_body.txt', context)

    def get_recovery_mail_html(self, context):
        return render_to_string('auth_registration/_activation_mail_body.html', context)


class ConfirmationView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        code = self.kwargs['code']
        try:
            user = ActivationCodeGenerator().decode(code)
            Activation.objects.create(user=user)
            messages.success(self.request, _("The user account has been activated. You can log in now."))
            return reverse("auth_factories:login")
        except (SignatureExpired, User.DoesNotExist):
            messages.warning(self.request, _("The link used by you is not valid. "
                                             "The activation link is valid for 7 days. Create new account."))
        except BadSignature:
            messages.warning(self.request, _("The link used by you is incorrect."))
        return reverse("home")
