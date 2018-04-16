# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-16 04:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    replaces = [('events', '0005_auto_20150503_1741'), ('events', '0006_remove_event_for_client'), ('events', '0007_reminder'), ('events', '0008_auto_20180415_1916'), ('events', '0009_auto_20180415_1922'), ('events', '0010_auto_20180415_1923')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('records', '0007_remove_record_alarm'),
        ('events', '0004_auto_20150322_0543'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alarm',
            options={'verbose_name': 'Alarm', 'verbose_name_plural': 'Alarms'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AlterField(
            model_name='event',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created on'),
        ),
        migrations.AlterField(
            model_name='event',
            name='deadline',
            field=models.BooleanField(default=False, verbose_name='Dead-line'),
        ),
        migrations.RemoveField(
            model_name='event',
            name='for_client',
        ),
        migrations.AlterField(
            model_name='event',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified by'),
        ),
        migrations.AlterField(
            model_name='event',
            name='modified_on',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Modified on'),
        ),
        migrations.AlterField(
            model_name='event',
            name='text',
            field=models.CharField(max_length=150, verbose_name='Subject'),
        ),
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.DateTimeField(verbose_name='Time'),
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('user', models.ForeignKey(help_text='Recipient', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('active', models.BooleanField(default=True, help_text='Active status')),
            ],
            options={
                'verbose_name': 'Reminder',
                'verbose_name_plural': 'Reminders',
            },
        ),
        migrations.RemoveField(
            model_name='alarm',
            name='case',
        ),
        migrations.RemoveField(
            model_name='alarm',
            name='event',
        ),
        migrations.DeleteModel(
            name='Alarm',
        ),
    ]