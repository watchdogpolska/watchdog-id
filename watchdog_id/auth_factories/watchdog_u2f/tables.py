from django_tables2 import tables, TemplateColumn

from watchdog_id.auth_factories.watchdog_u2f.models import U2FToken


class U2FTokenTable(tables.Table):
    action = TemplateColumn(template_name='watchdog_u2f/_u2ftoken_table.html')

    class Meta:
        model = U2FToken
        template = 'django_tables2/bootstrap-responsive.html'
        fields = ['device_name', 'last_used', 'created']
