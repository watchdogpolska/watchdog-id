from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel
import jsonfield

EVENT_LABELS = {'user_authenticated': _("User authenticated"),
                'user_identified': _("User identified"),
                'factory_authenticated': _("Factory authenticated"),
                'user_logout': _("User logout")}


class LogEntryQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class LogEntry(TimeStampedModel):
    event_type = models.CharField(verbose_name=_("Event type"), max_length=150)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True,
                             related_name='auth_log_entries')
    session_key = models.CharField(verbose_name=_("Session ID"), max_length=40, blank=True)
    request_ip = models.GenericIPAddressField(verbose_name=_("IP Address"))
    extra_data = jsonfield.JSONField(verbose_name=_("Extra data"),
                                     help_text=_("Values depending on the type of event."))
    objects = LogEntryQuerySet.as_manager()

    @property
    def event_label(self):
        return EVENT_LABELS.get(self.event_type, self.event_type)

    class Meta:
        verbose_name = _("Log Entry")
        verbose_name_plural = _("Log Entries")
        ordering = ['created', ]

    def __str__(self):
        return "Event[type={}, created={}, user_id={}]".format(self.event_type, self.created, self.user_id)

    def get_absolute_url(self):
        return reverse('auth_local_log:details', kwargs={'pk': str(self.pk)})
