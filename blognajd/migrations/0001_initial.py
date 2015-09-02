# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django_markup.fields
import inline_media.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique_for_date='pub_date')),
                ('markup', django_markup.fields.MarkupField(choices=[('none', 'None (no processing)'), ('linebreaks', 'Linebreaks'), ('markdown', 'Markdown'), ('restructuredtext', 'reStructuredText')], max_length=255, default='markdown', verbose_name='markup')),
                ('abstract', inline_media.fields.TextFieldWithInlines()),
                ('abstract_markup', models.TextField(null=True, blank=True)),
                ('body', inline_media.fields.TextFieldWithInlines()),
                ('body_markup', models.TextField(null=True, blank=True)),
                ('status', models.IntegerField(choices=[(1, 'Draft'), (2, 'Public')], default=1)),
                ('allow_comments', models.BooleanField(default=True)),
                ('pub_date', models.DateField(default=datetime.date(2015, 8, 24), verbose_name='Publication date')),
                ('mod_date', models.DateField(auto_now=True, verbose_name='Modification date')),
                ('visits', models.IntegerField(editable=False, default=0)),
                ('tags', taggit.managers.TaggableManager(through='taggit.TaggedItem', help_text='A comma-separated list of tags.', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'permissions': (('can_see_unpublished_stories', 'Can see unpublished stories'),),
                'ordering': ('-pub_date',),
                'get_latest_by': 'pub_date',
                'verbose_name_plural': 'stories',
                'db_table': 'blog_stories',
                'verbose_name': 'story',
            },
        ),
    ]
