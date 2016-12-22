from oauth2_provider.models import get_application_model
from atom.ext.crispy_forms.forms import HelperMixin, SingleButtonMixin
from django import forms


class ApplicationForm(SingleButtonMixin, forms.ModelForm):
    STANDARD_FIELD = ('name', 'client_id', 'client_secret', 'client_type',
                      'authorization_grant_type', 'redirect_uris')

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:  # Create form
            for fieldname in self.fields.keys():
                if fieldname not in self.STANDARD_FIELD:
                    del self.fields[fieldname]

    class Meta:
        model = get_application_model
        fields = ('name', 'client_id', 'client_secret', 'client_type',
                  'authorization_grant_type', 'redirect_uris', 'skip_authorization')
