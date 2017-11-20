from atom.ext.crispy_forms.forms import SingleButtonMixin
from atom.views import ActionView
from django import forms
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.views.generic import FormView, ListView, TemplateView
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories import set_identified_user, get_identified_user, Registry, unset_user
from watchdog_id.auth_factories.models import Factor
from watchdog_id.users.models import User


class UserForm(SingleButtonMixin, forms.Form):
    action_text = _("Log in")
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  to_field_name='username',
                                  widget=forms.widgets.TextInput(),
                                  empty_label=None,
                                  label=_("Username"))


class LoginFormView(FormView):
    form_class = UserForm
    template_name = "auth_factories/login_form.html"

    def form_valid(self, form):
        set_identified_user(self.request, form.cleaned_data['user'])
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('auth_factories:list')


class FactorListView(ListView):
    model = Factor

    @cached_property
    def identified_user(self):
        return get_identified_user(self.request)

    def dispatch(self, request, *args, **kwargs):
        if self.identified_user is None:
            messages.warning(self.request, _("You must first identify yourself."))
            return redirect(reverse('auth_factories:login'))
        if not self.request.user.is_anonymous():
            messages.warning(self.request, _("You do not need to authenticate more."))
            return redirect(self.request.session.get('success_url', reverse('home')))

        return super(FactorListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(FactorListView, self).get_queryset()

    def get_context_data(self, **kwargs):
        kwargs['factory_list'] = self.get_factory_list()
        kwargs['registry'] = Registry
        kwargs['identified_user'] = self.identified_user
        return super(FactorListView, self).get_context_data(**kwargs)

    def get_factory_list(self):
        data = []
        for _, config in Registry.items():
            data.append((config.name, config.get_authentication_url()))
        return data


class LogoutForm(SingleButtonMixin, forms.Form):
    action_text = _("Log out")


class LogoutActionView(FormView):
    form_class = LogoutForm
    template_name = "auth_factories/logout.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, _("The user is logged out correctly."))
        unset_user(self.request)
        return super(LogoutActionView, self).form_valid(form)
