from django.contrib import admin

# Register your models here.

from .models import ProcessDefinition

admin.site.register(ProcessDefinition)
