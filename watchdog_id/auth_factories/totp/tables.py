from django_tables2 import tables, A, LinkColumn, TemplateColumn
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.totp.models import OTPPassword


class OTPPasswordTable(tables.Table):
    delete = TemplateColumn(template_name='totp/_otpassword_table.html')

    class Meta:
        model = OTPPassword
        template = 'django_tables2/bootstrap-responsive.html'
        fields = ('device_name', 'last_used', 'created', 'modified')
