from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username

# This signal automatically creates a UserProfile and an Auth Token for every new user.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_and_token(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Token.objects.create(user=instance)