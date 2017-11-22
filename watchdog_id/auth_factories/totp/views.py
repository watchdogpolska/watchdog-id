import pyotp
from atom.ext.crispy_forms.forms import SingleButtonMixin
from atom.views import DeleteMessageMixin
from braces.forms import UserKwargModelFormMixin
from braces.views import LoginRequiredMixin, FormValidMessageMixin, UserFormKwargsMixin
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from .models import OTPPassword


class OTPPasswordForm(forms.ModelForm):
    class Meta:
        model = OTPPassword
        fields = ('device_name',)


class CreateOTPPasswordForm(SingleButtonMixin, UserKwargModelFormMixin, forms.ModelForm):
    token = forms.CharField(label=_("Token"))

    def clean_token(self):
        token = self.cleaned_data['token']
        shared_secret = self.cleaned_data['shared_secret']
        totp = pyotp.TOTP(shared_secret)
        if not totp.verify(token):
            raise forms.ValidationError(_("The token you entered is invalid. Hurry up and try again."))

    def save(self, commit=True):
        self.instance.user = self.user
        return super(CreateOTPPasswordForm, self).save(commit)

    class Meta:
        model = OTPPassword
        fields = ('device_name', 'shared_secret')
        widgets = {
            'shared_secret': forms.TextInput(attrs={'readonly': True}),
        }


class UserQuerysetMixin(object):
    def get_queryset(self):
        return super(UserQuerysetMixin, self).get_queryset().filter(user=self.request.user)


class OTPPasswordListView(UserQuerysetMixin, ListView):
    model = OTPPassword


class OTPPasswordDetailView(UserQuerysetMixin, LoginRequiredMixin, DetailView):
    model = OTPPassword


class OTPPasswordCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = OTPPassword
    form_class = CreateOTPPasswordForm

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class OTPPasswordUpdateView(LoginRequiredMixin, UserQuerysetMixin, UserFormKwargsMixin,
                            FormValidMessageMixin, UpdateView):
    model = OTPPassword
    form_class = OTPPasswordForm

    def get_form_valid_message(self):
        return _("{0} updated!").format(self.object)


class OTPPasswordDeleteView(LoginRequiredMixin, DeleteMessageMixin, DeleteView):
    model = OTPPassword
    success_url = reverse_lazy('auth_factories:totp:list')

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)


class AuthenticationView(View):
    pass
