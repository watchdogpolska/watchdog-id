import logging
import random

from atom.ext.crispy_forms.forms import SingleButtonMixin
from atom.views import DeleteMessageMixin
from braces.views import FormValidMessageMixin
from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, FormView
from django_tables2 import SingleTableView, TemplateColumn, tables

from watchdog_id.auth_factories.mixins import UserFormKwargsMixin, SingleFactoryProcessMixin, SettingsViewMixin, \
    SettingsFactoryView
from watchdog_id.auth_factories.sms_code.factory import SmsCodeFactory
from watchdog_id.auth_factories.sms_code.settings import FROM_NUMBER, MAX_BID
from watchdog_id.auth_factories.sms_code.utils import get_client
from watchdog_id.auth_factories.views import FinishAuthenticationFormView
from .models import PhoneNumber

logger = logging.getLogger(__name__)


class UserQuerysetMixin(object):
    def get_queryset(self):
        return super(UserQuerysetMixin, self).get_queryset().filter(user=self.request.user)


class PhoneNumberTable(tables.Table):
    action = TemplateColumn(template_name='auth_factories/_default/_action_table.html',
                            context={'update_viewname': 'auth_factories:sms_code:update',
                                     'delete_viewname': 'auth_factories:sms_code:delete'})

    class Meta:
        model = PhoneNumber
        template = 'django_tables2/bootstrap-responsive.html'
        fields = ('phone', 'last_used',)


class PhoneNumberListView(SettingsFactoryView, UserQuerysetMixin, SingleTableView):
    model = PhoneNumber
    factory = SmsCodeFactory
    table_class = PhoneNumberTable


class PhoneNumberDetailView(SettingsFactoryView, UserQuerysetMixin, DetailView):
    factory = SmsCodeFactory
    model = PhoneNumber


class PhoneNumberForm(SingleButtonMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PhoneNumberForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.user = self.user
        return super().save(commit)

    class Meta:
        model = PhoneNumber
        fields = ['phone', ]


class PhoneNumberCreateView(SettingsFactoryView, UserFormKwargsMixin, CreateView):
    model = PhoneNumber
    factory = SmsCodeFactory
    form_class = PhoneNumberForm
    success_url = reverse_lazy('auth_factories:sms_code:list')

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class PhoneNumberUpdateView(SettingsFactoryView, UserQuerysetMixin, UserFormKwargsMixin, FormValidMessageMixin,
                            UpdateView):
    model = PhoneNumber
    factory = SmsCodeFactory
    form_class = PhoneNumberForm

    def get_form_valid_message(self):
        return _("{0} updated!").format(self.object)


class PhoneNumberDeleteView(SettingsFactoryView, UserQuerysetMixin, DeleteMessageMixin, DeleteView):
    model = PhoneNumber
    success_url = reverse_lazy('auth_factories:sms_code:list')
    factory = SmsCodeFactory

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)


class SecurePhoneNumberField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('queryset', PhoneNumber.objects.none()),
        kwargs.setdefault('label', _("Phone"))
        kwargs.setdefault('required', True)
        self.start_show = kwargs.pop('start_show', 4)
        self.end_show = kwargs.pop('end_show', 2)
        super(SecurePhoneNumberField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        phone = "{}".format(obj.phone)
        return phone[:self.start_show] + \
               "*" * (len(phone) - self.start_show - self.end_show) + \
               phone[-self.end_show:]


class SelectPhoneForm(SingleButtonMixin, forms.Form):
    action_text = _("Send SMS code")
    phone = SecurePhoneNumberField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(SelectPhoneForm, self).__init__(*args, **kwargs)
        self.fields['phone'].queryset = PhoneNumber.objects.for_user(self.user).all()


class CodeSessionManager(object):
    PHONE_KEY = '2fa:sms_code:phone'
    CODE_KEY = '2fa:sms_code:code'

    def __init__(self, session):
        self.session = session

    def reset_session_code(self, phone):
        session_code = random.randint(1000, 9999)
        self.session[self.CODE_KEY] = session_code
        self.session[self.PHONE_KEY] = phone.pk

    def get_code(self, phone):
        if self.CODE_KEY not in self.session or self.session.get(self.PHONE_KEY, None) != phone.pk:
            self.reset_session_code(phone)
        return self.session[self.CODE_KEY]


class SelectPhoneView(SingleFactoryProcessMixin, FormView):
    form_class = SelectPhoneForm
    factory = SmsCodeFactory
    template_name = 'auth_factories/_default/authentication.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user_manager.get_identified_user()
        return kwargs

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('auth_factories:sms_code:index',
                       kwargs={'phone_id': self.form.cleaned_data['phone'].pk})


class ValidateCodeForm(SingleButtonMixin, forms.Form):
    code = forms.CharField(label=_("Code"))

    error_messages = {'invalid_code': _("The entered code is incorrect. Try again.")}

    def __init__(self, *args, **kwargs):
        self.code = kwargs.pop('code')
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data['code']
        if str(self.code) != code:
            raise forms.ValidationError(self.error_messages['invalid_code'])
        return code


class ValidateCodeView(SingleFactoryProcessMixin, FinishAuthenticationFormView,
                       FormView):
    form_class = ValidateCodeForm
    factory = SmsCodeFactory
    template_name = 'auth_factories/_default/authentication.html'
    client = get_client()
    success_message = _("SMS authentication success.")

    def dispatch(self, request, *args, **kwargs):
        self.session_manager = CodeSessionManager(request.session)
        return super(ValidateCodeView, self).dispatch(request, *args, **kwargs)

    @cached_property
    def phone(self):
        return get_object_or_404(PhoneNumber.objects.
                                 for_user(self.user_manager.get_identified_user()),
                                 pk=self.kwargs['phone_id'])

    def get(self, request, *args, **kwargs):
        self.session_manager.reset_session_code(self.phone)
        self.send_notification()
        return super(ValidateCodeView, self).get(request, *args, **kwargs)

    def send_notification(self):
        code = self.session_manager.get_code(self.phone)
        phone = self.phone
        site = get_current_site(self.request)
        self.send_sms(code, phone, site)

    def send_sms(self, code, phone, site):
        msg = _("{} enter on {} during authentication.").format(code, site.name)
        logger.info("The authentication code to {} was send.".format(phone))
        self.client.messages.create(to=phone,
                                    from_=FROM_NUMBER,
                                    max_rate=MAX_BID,
                                    body=msg)

    def get_form_kwargs(self):
        kwargs = super(ValidateCodeView, self).get_form_kwargs()
        kwargs['user'] = self.user_manager.get_identified_user()
        kwargs['code'] = self.session_manager.get_code(self.phone)
        return kwargs

    def form_valid(self, form):
        response = super(ValidateCodeView, self).form_valid(form)
        self.phone.last_used = now()
        self.phone.save()
        self.session_manager.reset_session_code(self.phone)
        return response
