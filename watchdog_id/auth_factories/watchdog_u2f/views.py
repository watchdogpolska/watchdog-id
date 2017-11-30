# -*- coding: utf-8 -*-

from atom.views import DeleteMessageMixin
from braces.views import UserFormKwargsMixin
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django_tables2 import SingleTableView

from watchdog_id.auth_factories.mixins import SettingsViewMixin, AuthenticationProcessMixin
from watchdog_id.auth_factories.views import AuthenticationFormView
from watchdog_id.auth_factories.watchdog_u2f.factory import WatchdogU2FFactory
from watchdog_id.auth_factories.watchdog_u2f.forms import U2FTokenForm, U2FTokenCreateForm, U2FTokenAuthenticationForm
from watchdog_id.auth_factories.watchdog_u2f.models import U2FToken
from watchdog_id.auth_factories.watchdog_u2f.tables import U2FTokenTable


class UserQuerysetMixin(object):
    def get_queryset(self):
        return super(UserQuerysetMixin, self).get_queryset().filter(user=self.request.user)


class U2FTokenListView(SettingsViewMixin, UserQuerysetMixin, SingleTableView):
    model = U2FToken
    table_class = U2FTokenTable


class U2FTokenCreateView(SettingsViewMixin, UserFormKwargsMixin, CreateView):
    form = U2FTokenCreateForm
    form_class = U2FTokenCreateForm
    model = U2FToken

    def get_success_message(self):
        return _("{0} created!").format(self.object)


class U2FTokenDetailsView(SettingsViewMixin, UserQuerysetMixin, DetailView):
    model = U2FToken


class U2FTokenUpdateView(SettingsViewMixin, UserQuerysetMixin, UpdateView):
    model = U2FToken
    form_class = U2FTokenForm


class U2FTokenDeleteView(SettingsViewMixin, DeleteMessageMixin, DeleteView):
    model = U2FToken
    success_url = reverse_lazy('auth_factories:u2ftoken:list')
    form_class = U2FTokenForm


class AuthenticationView(AuthenticationProcessMixin, AuthenticationFormView):
    form_class = U2FTokenAuthenticationForm
    factory = WatchdogU2FFactory
    success_message = _("U2F authentication succeeded.")
    template_name = 'watchdog_u2f/authentication.html'

    def get_form_kwargs(self):
        kwargs = super(AuthenticationView, self).get_form_kwargs()
        kwargs['user'] = self.request.user_manager.get_identified_user()
        return kwargs

    def form_valid(self, form):
        form.cleaned_data['token'].last_used = now()
        form.cleaned_data['token'].save()
        return super(AuthenticationView, self).form_valid(form)
