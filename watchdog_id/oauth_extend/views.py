from oauth2_provider.views import ApplicationRegistration
from django.contrib.auth.mixins import PermissionRequiredMixin


class ProtectedApplicationRegistration(PermissionRequiredMixin, ApplicationRegistration):
    permission_required = ['oauth2_provider.add_application']
