# Generated by Django 2.2 on 2022-07-13 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20220713_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Send_email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='activate_token',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='activated',
            field=models.BooleanField(default=False),
        ),
    ]
