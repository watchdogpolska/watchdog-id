from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django_tables2 import SingleTableView, tables, LinkColumn

from watchdog_id.auth_factories.mixins import SettingsViewMixin
from .models import LogEntry


class UserQuerysetMixin(object):
    def get_queryset(self):
        return super(UserQuerysetMixin, self).get_queryset().filter(user=self.request.user)


class LogEntryTable(tables.Table):
    created = LinkColumn(None)

    class Meta:
        model = LogEntry
        template = 'django_tables2/bootstrap-responsive.html'
        fields = ['created', 'event_label', 'session_key', ]


class LogEntryListView(SettingsViewMixin, UserQuerysetMixin, SingleTableView):
    model = LogEntry
    table_class = LogEntryTable


class LogEntryDetailView(SettingsViewMixin, UserQuerysetMixin, DetailView):
    model = LogEntry
