from django.contrib import admin

# Register your models here.

from .models import Operation, OperationVersion

admin.site.register(Operation)
admin.site.register(OperationVersion)
