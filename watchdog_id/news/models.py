from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField
from model_utils import Choices


class PostQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Post(TimeStampedModel):
    STATUS = Choices('draft', 'published')
    title = models.CharField(verbose_name=_("Title"), max_length=50)
    slug = models.SlugField(verbose_name=_("Slug"), unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = StatusField()
    published_at = MonitorField(monitor='status', when=['published'])
    content = HTMLField()
    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['created', ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:details', kwargs={'slug': self.slug,
                                               'month': str(self.published_at.month),
                                               'year': str(self.published_at.year),
                                               })
