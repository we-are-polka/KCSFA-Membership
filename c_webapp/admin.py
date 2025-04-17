from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Profile, Event, EventCategory, CPDLog

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(ModelAdmin):
    pass

@admin.register(EventCategory)
class EventCategoryAdmin(ModelAdmin):
    pass

@admin.register(CPDLog)
class CPDLogAdmin(ModelAdmin):
    pass
