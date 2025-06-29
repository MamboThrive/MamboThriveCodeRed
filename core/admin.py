from django.contrib import admin
from .models import TimelineEvent

@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'title', 'timestamp', 'related_object')
    list_filter = ('event_type',)
    search_fields = ('title', 'summary', 'user__username')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
