from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ProcessDefinition(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey('auth.User', related_name='process_definitions')
    definition = models.TextField()

    @property
    def __str__(self):
        return self.name

