# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blognajd', '0003_sitesettings_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='has_about_page',
            field=models.BooleanField(help_text='has_about_page', default=True),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='has_contact_page',
            field=models.BooleanField(help_text='has_contact_page', default=True),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='has_projects_page',
            field=models.BooleanField(help_text='has_projects_page', default=True),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='meta_author',
            field=models.CharField(help_text='meta_author', max_length=48, blank=True, verbose_name='Meta author', default='meta author'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='meta_description',
            field=models.TextField(help_text='meta_description', blank=True, verbose_name='Long description of the site', default='meta description'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='meta_keywords',
            field=models.CharField(help_text='meta_keywords', max_length=256, blank=True, verbose_name='Meta keywords', default='meta keywords'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='paginate_by',
            field=models.PositiveSmallIntegerField(help_text='Number of stories per page (paginate_by)', verbose_name='Paginate by', default=10),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='site_long_name',
            field=models.CharField(help_text='site_long_name', max_length=256, blank=True, verbose_name='Site long name', default='longname'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='site_short_name',
            field=models.CharField(help_text='short_short_name', max_length=48, verbose_name='Site short name', default='sitename'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='theme',
            field=models.CharField(help_text='theme', max_length=24, verbose_name='Theme', default='default'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='truncate_to',
            field=models.PositiveSmallIntegerField(help_text="number of words stories' abstracts get truncated to (truncate_to)", verbose_name='Truncate to', default=200),
        ),
    ]
