import random
import string

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


def secure_string(length):
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(length))


class RecoveryCode(TimeStampedModel):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    code = models.CharField(verbose_name=_('Code'), max_length=128)

    def check_code(self, code):
        return check_password(code, self.code)

    def generate_code(self):
        code = secure_string(16)
        self.code = make_password(code)
        return code
