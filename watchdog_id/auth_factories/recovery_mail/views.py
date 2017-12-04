from atom.ext.crispy_forms.forms import SingleButtonMixin
from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView

from watchdog_id.auth_factories.mixins import AuthenticationProcessMixin, SingleFactoryProcessMixin
from watchdog_id.auth_factories.recovery_mail.factory import RecoveryMailFactory
from watchdog_id.auth_factories.recovery_mail.models import RecoveryCode
from watchdog_id.auth_factories.views import FinishAuthenticationFormView


class RecoveryCodeCreateForm(SingleButtonMixin, forms.ModelForm):
    action_text = _("Send code")
    email = forms.CharField(label=_("Enter the e-mail address provided when the account was created"))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(RecoveryCodeCreateForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not self.user.email == email:
            raise forms.ValidationError(_("The email address provided is not valid."))
        return email

    def save(self, commit=True):
        self.instance.user = self.user
        self.code = self.instance.generate_code()
        return super().save(commit)

    class Meta:
        model = RecoveryCode
        fields = []


class EmailSendView(SingleFactoryProcessMixin, SuccessMessageMixin, CreateView):
    form_class = RecoveryCodeCreateForm
    factory = RecoveryMailFactory
    model = RecoveryCode
    success_message = _("The confirmation code was sent to the e-mail address provided during registration.")
    success_url = reverse_lazy('auth_factories:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user_manager.get_identified_user()
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_recovery_mail(form, self.object)
        return response

    def send_recovery_mail(self, form, recovery_code):
        context = self.get_recovery_mail_context(form.code, recovery_code)
        recovery_code.user.email_user(subject=_("Restoring account access"),
                                      message=self.get_recovery_mail_txt(context),
                                      html_message=self.get_recovery_mail_html(context))

    def get_recovery_mail_context(self, code, recovery_code):
        url = reverse('auth_factories:recovery_mail:confirmation',
                      kwargs={'code': code,
                              'request_id': recovery_code.pk})
        url = self.request.build_absolute_uri(url)
        return {'user': recovery_code.user,
                'code': code,
                'site': get_current_site(self.request),
                'url': url}

    def get_recovery_mail_txt(self, context):
        return render_to_string('recovery_mail/_recovery_mail_body.txt', context)

    def get_recovery_mail_html(self, context):
        return render_to_string('recovery_mail/_recovery_mail_body.html', context)


class RecoveryCodeVerifyForm(SingleButtonMixin, forms.Form):
    action_text = _("Authenticate")
    error_messages = {'invalid_request': _("The link used is not valid. The posted link is valid "
                                           "for 24 hours. Try again."),
                      'invalid_code': _("The link used is not valid. The posted link is valid "
                                        "for 24 hours. Try again.")}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.request = kwargs.pop('request_id')
        self.code = kwargs.pop('code')
        super(RecoveryCodeVerifyForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RecoveryCodeVerifyForm, self).clean()
        try:
            rc = RecoveryCode.objects.get(pk=self.request)
            if not rc.check_code(self.code):
                raise forms.ValidationError(self.error_messages['invalid_code'])
        except RecoveryCode.DoesNotExist:
            raise forms.ValidationError(self.error_messages['invalid_request'])
        return cleaned_data


class EmailConfirmationView(SingleFactoryProcessMixin, FinishAuthenticationFormView):
    factory = RecoveryMailFactory
    form_class = RecoveryCodeVerifyForm
    success_message = _("E-mail authentication succeeded.")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request_id'] = self.kwargs['request_id']
        kwargs['code'] = self.kwargs['code']
        kwargs['user'] = self.user_manager.get_identified_user()
        return kwargs
