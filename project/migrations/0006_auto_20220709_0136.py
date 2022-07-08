# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-07-08 17:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20220709_0122'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('url', models.TextField()),
            ],
            options={
                'db_table': 'top_sites',
            },
        ),
        migrations.RemoveField(
            model_name='order',
            name='memory_capacity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='top_sites',
        ),
        migrations.RemoveField(
            model_name='order',
            name='used_memory',
        ),
        migrations.AddField(
            model_name='topsite',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Order'),
        ),
    ]