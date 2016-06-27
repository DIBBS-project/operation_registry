from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.


class ProcessDefinition(models.Model):
    name = models.CharField(max_length=256)
    author = models.ForeignKey('auth.User', related_name='process_definitions')
    appliance = models.CharField(max_length=256)
    archive_url = models.URLField()
    creation_date = models.DateTimeField(auto_now_add=True)
    adapters = JSONField()

    @property
    def __str__(self):
        return self.name


# Add a token upon user creation
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(author=instance)
