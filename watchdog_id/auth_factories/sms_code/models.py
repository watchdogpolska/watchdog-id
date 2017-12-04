from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField


class PhoneNumberQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)


@python_2_unicode_compatible
class PhoneNumber(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True)
    last_used = models.DateTimeField(null=True, blank=True)
    objects = PhoneNumberQuerySet.as_manager()

    class Meta:
        verbose_name = _("Phone Number")
        verbose_name_plural = _("Phone Numbers")
        ordering = ['created', ]

    def __str__(self):
        return "{}".format(self.phone)

    def get_absolute_url(self):
        return reverse('auth_factories:sms_code:details', kwargs={'pk': self.pk})
