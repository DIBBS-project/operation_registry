from django.db import models
from django.contrib.auth.models import User


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.


class ProcessDefinition(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey('auth.User', related_name='process_definitions')
    definition = models.TextField()

    @property
    def __str__(self):
        return self.name


# Add a token upon user creation
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
