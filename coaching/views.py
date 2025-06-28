from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import HealthGoal, CoachMessage

@login_required
def coaching_view(request):
    goals = HealthGoal.objects.filter(user=request.user).order_by('-start_date')
    messages = CoachMessage.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'coaching/coaching.html', {'goals': goals, 'messages': messages})
