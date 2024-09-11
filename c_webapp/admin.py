from django.contrib import admin
from .models import Profile, Event, EventCategory, CPDLog

# Register your models here.
admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(CPDLog)