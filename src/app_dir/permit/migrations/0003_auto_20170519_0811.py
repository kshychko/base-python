# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-19 08:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20170519_0811'),
        ('permit', '0002_filestorage_inspections_permitextclassa_permitextclassb_supportingfiles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('applicant', jsonfield.fields.JSONField(default={}, help_text='Applicant')),
                ('agent', jsonfield.fields.JSONField(default={}, help_text='Agent')),
                ('recipient', jsonfield.fields.JSONField(default={}, help_text='Recipient')),
                ('transport', jsonfield.fields.JSONField(default={}, help_text='Transport')),
                ('goods_a', jsonfield.fields.JSONField(default={}, help_text='Goods (A)')),
                ('goods_b', jsonfield.fields.JSONField(default={}, help_text='Goods (B)')),
                ('applicant_name', models.CharField(help_text='Applicant Name', max_length=70)),
                ('permit_number', models.CharField(blank=True, help_text='Permit No', max_length=10)),
                ('valid_from', models.DateField(help_text='Valid From')),
                ('valid_to', models.DateField(help_text='Valid To')),
                ('assessment_date', models.DateField(blank=True, help_text='Assessment Date')),
                ('assessment', models.TextField(blank=True, help_text='Assessment')),
                ('delegate_date', models.DateField(blank=True, help_text='Delegate Date')),
                ('status', models.SmallIntegerField(choices=[(1, 'New'), (2, 'Pending'), (3, 'Approved')], default=1, help_text='Status')),
                ('assessor', models.ForeignKey(blank=True, help_text='Assessor', on_delete=django.db.models.deletion.CASCADE, related_name='accessor', to='account.Account')),
                ('delegate', models.ForeignKey(blank=True, help_text='Delegate', on_delete=django.db.models.deletion.CASCADE, related_name='delegate', to='account.Account')),
            ],
            options={
                'verbose_name': 'Application',
                'verbose_name_plural': 'Applications',
            },
        ),
        migrations.CreateModel(
            name='ApplicationStatusChange',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('action_date', models.DateField(help_text='Date of action')),
                ('new_status', models.SmallIntegerField(choices=[(1, 'New'), (2, 'Pending'), (3, 'Approved')], help_text='New status set')),
                ('notes', models.TextField(help_text='Notes')),
                ('application', models.ForeignKey(help_text='Application', on_delete=django.db.models.deletion.CASCADE, to='permit.Application')),
                ('staff', models.ForeignKey(help_text='Staff Account', on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
            options={
                'verbose_name': 'Application Status Change',
                'verbose_name_plural': 'Application Status Changes',
            },
        ),
        migrations.RemoveField(
            model_name='permit',
            name='agent_country',
        ),
        migrations.RemoveField(
            model_name='permit',
            name='agent_state',
        ),
        migrations.RemoveField(
            model_name='permit',
            name='agent_suburb',
        ),
        migrations.RemoveField(
            model_name='permit',
            name='applicant_country',
        ),
        migrations.RemoveField(
            model_name='permit',
            name='applicant_state',
        ),
        migrations.RemoveField(
            model_name='permit',
            name='applicant_suburb',
        ),
        migrations.RemoveField(
            model_name='permit',
            name='assessor',
        ),
        migrations.RemoveField(
            model_name='permit',
            name='delegate',
        ),
        migrations.RemoveField(
            model_name='permit',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='permit',
            name='origin',
        ),
        migrations.RemoveField(
            model_name='permit',
            name='recipient_country',
        ),
        migrations.RemoveField(
            model_name='permit',
            name='recipient_state',
        ),
        migrations.RemoveField(
            model_name='permit',
            name='recipient_suburb',
        ),
        migrations.DeleteModel(
            name='PermitExtClassA',
        ),
        migrations.DeleteModel(
            name='PermitExtClassB',
        ),
        migrations.RemoveField(
            model_name='permitstatuschange',
            name='permit',
        ),
        migrations.RemoveField(
            model_name='permitstatuschange',
            name='staff',
        ),
        migrations.AlterModelOptions(
            name='filestorage',
            options={'verbose_name': 'File Storage', 'verbose_name_plural': 'File Storages'},
        ),
        migrations.AlterModelOptions(
            name='inspections',
            options={'verbose_name': 'Inspection', 'verbose_name_plural': 'Inspections'},
        ),
        migrations.AlterModelOptions(
            name='supportingfiles',
            options={'verbose_name': 'Supporting File', 'verbose_name_plural': 'Supporting Files'},
        ),
        migrations.RemoveField(
            model_name='inspections',
            name='permit',
        ),
        migrations.AddField(
            model_name='inspections',
            name='goods_a',
            field=jsonfield.fields.JSONField(default={}, help_text='Goods (A)'),
        ),
        migrations.AddField(
            model_name='inspections',
            name='goods_b',
            field=jsonfield.fields.JSONField(default={}, help_text='Goods (B)'),
        ),
        migrations.AlterField(
            model_name='inspections',
            name='inspection_date',
            field=models.DateField(auto_now_add=True, help_text='Inspection date'),
        ),
        migrations.AlterField(
            model_name='inspections',
            name='inspection_officer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inspections', to='account.Account'),
        ),
        migrations.DeleteModel(
            name='Permit',
        ),
        migrations.DeleteModel(
            name='PermitStatusChange',
        ),
        migrations.AddField(
            model_name='inspections',
            name='application',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inspections', to='permit.Application'),
        ),
    ]
