from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel


class ActivationQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Activation(TimeStampedModel):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    objects = ActivationQuerySet.as_manager()

    class Meta:
        verbose_name = _("Activation")
        verbose_name_plural = _("Activations")
        ordering = ['created', ]
