# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-07-08 17:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20220709_0053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='capacity_memory',
            new_name='memory_capacity',
        ),
    ]
