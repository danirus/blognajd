# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blognajd', '0002_auto_20150825_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='theme',
            field=models.CharField(max_length=24, default='default', verbose_name='Theme'),
        ),
    ]
