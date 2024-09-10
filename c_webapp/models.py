from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime
from django.utils import timezone

# Create your models here.

# User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='profile_pics/', default='default-profile.jpg')
    membership_status = models.CharField(max_length=20, default="Active")  # Active, Inactive, etc.
    total_cpd_points = models.IntegerField(default=0)  # Tracks total points for each member

    def __str__(self):
        return self.user.username
    
# Create a user profile by default when a user signs up
def create_profile(sender, instance, created, **kwargs)    :
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

# Automate the profile thing        
post_save.connect(create_profile, sender=User)


# Event Category (CPD Categories)
class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    points_per_event = models.IntegerField()  # Points allocated per event in this category

    def __str__(self):
        return self.name


# Event or Training
class Event(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(Profile, through='CPDLog')  # Relates to attendees via CPDLog

    def __str__(self):
        return self.name    


# CPD Log (Tracks CPD points for each member attending events)
class CPDLog(models.Model):
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    points_earned = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.points_earned:
            # Automatically assign points based on event category
            self.points_earned = self.event.category.points_per_event
        super().save(*args, **kwargs)

        # Update total CPD points in member's profile
        self.member.total_cpd_points += self.points_earned
        self.member.save()

    def __str__(self):
        return f"{self.member.user.username} - {self.event.name} - {self.points_earned} Points"        