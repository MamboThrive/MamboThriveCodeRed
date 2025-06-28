from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TimelineEvent

@login_required
def timeline_view(request):
    events = TimelineEvent.objects.filter(user=request.user)
    return render(request, 'core/timeline.html', {'events': events})