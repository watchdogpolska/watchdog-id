from django.contrib import admin

# Register your models here.
from watchdog_id.auth_factories.models import Factor


@admin.register(Factor)
class FactoryAdmin(admin.ModelAdmin):
    pass
