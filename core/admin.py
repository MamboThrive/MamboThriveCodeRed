from django.contrib import admin
from .models import TimelineEvent

# Register TimelineEvent model
@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'timestamp')
    search_fields = ('user__username', 'event_type', 'summary')
    list_filter = ('event_type', 'timestamp')
