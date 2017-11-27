from django_tables2 import tables, TemplateColumn

from watchdog_id.auth_factories.yubico_otp.models import YubicoOTPDevice


class YubicoOTPDeviceTable(tables.Table):
    action = TemplateColumn(template_name='yubico_otp/_yubicootpdevice_table.html')

    class Meta:
        model = YubicoOTPDevice
        template = 'django_tables2/bootstrap-responsive.html'
        fields = ('device_name', 'device_id', 'last_used')
