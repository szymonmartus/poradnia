# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-29 06:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0032_auto_20170923_1238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='case',
            options={'ordering': ['last_send'], 'permissions': (('can_view', 'Can view'), ('can_assign', 'Can assign new permissions'), ('can_send_to_client', 'Can send text to client'), ('can_manage_permission', 'Can assign permission'), ('can_add_record', 'Can add record'), ('can_change_own_record', 'Can change own records'), ('can_change_all_record', 'Can change all records'), ('can_close_case', 'Can close case'), ('can_select_client', 'Can select client'))},
        ),
    ]