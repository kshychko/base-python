# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-19 08:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.ForeignKey(help_text='Role', on_delete=django.db.models.deletion.CASCADE, to='account.UserRole'),
        ),
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.ForeignKey(help_text='User', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='name',
            field=models.CharField(help_text='Role Name', max_length=20),
        ),
    ]
