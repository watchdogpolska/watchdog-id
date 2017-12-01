from atom.ext.crispy_forms.forms import SingleButtonMixin
from django import forms
from django.utils.translation import ugettext_lazy as _

from watchdog_id.users.models import User


class LogoutForm(SingleButtonMixin, forms.Form):
    action_text = _("Log out")


class UserForm(SingleButtonMixin, forms.Form):
    action_text = _("Log in")

    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  to_field_name='username',
                                  widget=forms.widgets.TextInput(),
                                  empty_label=None,
                                  label=_("Username"),
                                  error_messages={'invalid_choice': _('The username you entered is not valid. '
                                                                      'The specified user does not exist.')})
