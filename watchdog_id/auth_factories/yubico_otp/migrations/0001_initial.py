# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-27 03:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='YubicoOTPDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('device_id', models.CharField(help_text='Device ID', max_length=12)),
                ('device_name', models.CharField(default='Yubico Token', help_text='Affordable user name token', max_length=25)),
                ('last_used', models.DateTimeField(blank=True, help_text='Time of last use of the token', null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
                'verbose_name': 'Yubico OTP Device',
                'verbose_name_plural': 'Yubico OTP Devices',
            },
        ),
    ]