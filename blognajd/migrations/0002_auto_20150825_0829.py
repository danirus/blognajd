# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
        ('blognajd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(verbose_name='Created at', auto_now_add=True)),
                ('modified', models.DateTimeField(verbose_name='Last Updated', auto_now=True)),
                ('site_short_name', models.CharField(verbose_name='Site short name', max_length=48)),
                ('site_long_name', models.CharField(verbose_name='Site long name', max_length=256, blank=True)),
                ('meta_author', models.CharField(verbose_name='Meta author', max_length=48, blank=True)),
                ('meta_keywords', models.CharField(verbose_name='Meta keywords', max_length=256, blank=True)),
                ('meta_description', models.TextField(verbose_name='Long description of the site', blank=True)),
                ('paginate_by', models.PositiveSmallIntegerField(verbose_name='Paginate by', default=10, help_text='number of stories per page')),
                ('truncate_to', models.PositiveSmallIntegerField(verbose_name='Truncate to', default=200, help_text="number of words stories' abstracts get truncated to")),
                ('has_about_page', models.BooleanField(default=True)),
                ('has_projects_page', models.BooleanField(default=True)),
                ('has_contact_page', models.BooleanField(default=True)),
                ('site', models.OneToOneField(editable=False, to='sites.Site', related_name='usersettings', null=True)),
                ('user', models.ForeignKey(related_name='usersettings', to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'verbose_name': 'Site settings',
                'verbose_name_plural': 'Site settings',
            },
        ),
        migrations.AlterField(
            model_name='story',
            name='pub_date',
            field=models.DateField(verbose_name='Publication date', default=datetime.date.today),
        ),
    ]
