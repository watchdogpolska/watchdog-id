from django.contrib import admin

# Register your models here.
from watchdog_id.auth_oidc.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass
