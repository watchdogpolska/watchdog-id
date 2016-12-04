from atom.ext.guardian.tests import PermissionStatusMixin
from django.core.urlresolvers import reverse
from django.test import TestCase

from watchdog_id.users.factories import UserFactory


class ProtectedApplicationRegistrationTestCase(PermissionStatusMixin, TestCase):
    permission = ['oauth2_provider.add_application', ]
    status_no_permission = 302

    def setUp(self):
        self.user = UserFactory(username='john')

    def get_url(self):
        return reverse('oauth2_provider:register')
