from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from words.models import Word

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    favorites = models.ManyToManyField(Word)

    def __unicode__(self):
        return self.user.username
    
# Signals
#
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created: 
        profile, new = UserProfile.objects.get_or_create(user=instance)
        
