# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-01-22 08:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s3compat_osf_addon', '0002_auto_20180301_0356'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodesettings',
            name='folder_location',
            field=models.TextField(blank=True, null=True),
        ),
    ]
