# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-07-09 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_auto_20220710_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthdate',
            field=models.DateField(),
        ),
    ]
