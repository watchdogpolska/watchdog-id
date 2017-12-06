from django.contrib import admin

from watchdog_id.auth_local_log.models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    '''
        Admin View for LogEntry
    '''
    list_display = ('created', 'event_type', 'user', 'session_key', 'extra_data')
    list_filter = ('event_type', 'created')
    search_fields = ('session_key', )

    def get_readonly_fields(self, request, obj=None):
        return ([field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many])

    def has_add_permission(self, request):
        return False
