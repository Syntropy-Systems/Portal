# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-07-08 16:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20220709_0036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='remaining_memory',
            new_name='capacity_memory',
        ),
    ]