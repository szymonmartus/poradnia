# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='key',
            field=models.CharField(default=users.models.generate_api_key, verbose_name='Api-key', max_length=32, editable=False),
            preserve_default=True,
        ),
    ]
