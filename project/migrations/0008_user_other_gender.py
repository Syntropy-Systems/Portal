# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-07-09 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_auto_20220709_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='other_gender',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]