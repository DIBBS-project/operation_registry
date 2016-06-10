# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('appliance_id', models.IntegerField()),
                ('archive_url', models.URLField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('adapters', jsonfield.fields.JSONField(default=dict)),
                ('author', models.ForeignKey(related_name='process_definitions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
