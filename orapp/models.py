# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.db import models
from jsonfield import JSONField


class Operation(models.Model):
    name = models.CharField(max_length=256)
    logo_url = models.CharField(max_length=512, blank=True, default='')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='operation_definitions')
    description = models.TextField(blank=True, default='')
    string_parameters = JSONField(blank=True, default='[]')
    file_parameters = JSONField(blank=True, default='[]')


class OperationVersion(models.Model):
    name = models.CharField(max_length=256)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='process_implementations')
    operation = models.ForeignKey(Operation, related_name='implementations')
    appliance = models.CharField(max_length=256)
    creation_date = models.DateTimeField(auto_now_add=True)
    cwd = models.CharField(max_length=2048, blank=True, default='~')
    script = models.TextField()
    output_type = models.CharField(max_length=256)
    output_parameters = JSONField(blank=True, default='{}')
