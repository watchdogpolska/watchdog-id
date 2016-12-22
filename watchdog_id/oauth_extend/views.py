from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Button, Fieldset, Layout, Submit)
from crispy_forms.bootstrap import FormActions
from django.contrib.auth.mixins import PermissionRequiredMixin
from oauth2_provider.views import ApplicationRegistration


class ProtectedApplicationRegistration(PermissionRequiredMixin, ApplicationRegistration):
    permission_required = ['oauth2_provider.add_application']

    def get_helper(self):
        helper = FormHelper()
        helper.layout = Layout(
            Fieldset(
                'Application details',
                'name',
                'client_id',
                'client_secret',
                'client_type',
                'authorization_grant_type',
                'redirect_uris',
                'save',
            ),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel')
            )
        )
        return helper

    def get_context_data(self, **kwargs):
        context = super(ProtectedApplicationRegistration, self).get_context_data(**kwargs)
        context['helper'] = self.get_helper()
        return context
