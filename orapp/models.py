from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.


class Operation(models.Model):
    name = models.CharField(max_length=256)
    logo_url = models.CharField(max_length=512, blank=True, default='')
    author = models.ForeignKey('auth.User', related_name='operation_definitions')
    description = models.TextField(blank=True, default='')
    string_parameters = JSONField(blank=True, default='[]')
    file_parameters = JSONField(blank=True, default='[]')

    # @property
    # def __str__(self):
    #     return self.name


class OperationVersion(models.Model):
    name = models.CharField(max_length=256)
    author = models.ForeignKey('auth.User', related_name='process_implementations')
    operation = models.ForeignKey(Operation, related_name='implementations')
    appliance = models.CharField(max_length=256)
    creation_date = models.DateTimeField(auto_now_add=True)
    cwd = models.CharField(max_length=2048, blank=True, default='~')
    script = models.TextField()
    output_type = models.CharField(max_length=256)
    output_parameters = JSONField(blank=True, default='{}')


# Add a token upon user creation
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(author=instance)
