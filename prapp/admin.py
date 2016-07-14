from django.contrib import admin

# Register your models here.

from .models import ProcessDefinition, ProcessImplementation

admin.site.register(ProcessDefinition)
admin.site.register(ProcessImplementation)
