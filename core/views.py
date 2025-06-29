from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models.timeline import TimelineEvent
from django.utils import timezone
from django.db.models import Count

ICON_MAP = {
    'test_result': '🧪',
    'meal_log': '🥗',
    'sleep_log': '😴',
    'exercise': '🏃',
    'symptom': '🤒',
    'medication': '💊',
    'note': '📝',
    'goal': '🎯',
    'visit': '🩺',
    'other': '📌',
}

@login_required
def timeline_view(request):
    events = TimelineEvent.objects.filter(user=request.user)
    return render(request, 'core/timeline.html', {'events': events})

@login_required
def timeline_event_list(request):
    event_type = request.GET.get('type', '')
    events_qs = TimelineEvent.objects.filter(user=request.user)
    if event_type and event_type != 'all':
        events_qs = events_qs.filter(event_type=event_type)
    events = events_qs.order_by('-timestamp')
    # Get all event types with counts
    event_types = TimelineEvent.EVENT_TYPE_CHOICES
    type_counts = events_qs.values('event_type').annotate(count=Count('id'))
    type_count_map = {t['event_type']: t['count'] for t in type_counts}
    return render(request, 'core/timeline_events.html', {
        'events': events,
        'event_types': event_types,
        'active_type': event_type or 'all',
        'icon_map': ICON_MAP,
        'type_count_map': type_count_map,
    })