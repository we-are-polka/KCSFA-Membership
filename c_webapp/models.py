from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime

# Create your models here.

# User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='profile_pics/', default='default-profile.jpg')

    def __str__(self):
        return self.user.username
    
# Create a user profile by default when a user signs up
def create_profile(sender, instance, created, **kwargs)    :
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

# Automate the profile thing        
post_save.connect(create_profile, sender=User)