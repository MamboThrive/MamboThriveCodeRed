from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FoodLog
from .forms import FoodLogForm
from core.models.timeline import TimelineEvent
from django.contrib import messages
from django.utils import timezone
from datetime import date

@login_required
def food_log_view(request):
    # Default to today, or get date from GET param
    selected_date = request.GET.get('date')
    if selected_date:
        try:
            selected_date = date.fromisoformat(selected_date)
        except Exception:
            selected_date = timezone.localdate()
    else:
        selected_date = timezone.localdate()

    # Handle form submission
    if request.method == 'POST':
        form = FoodLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            # Set timestamp to selected date at noon for consistency
            log.timestamp = timezone.make_aware(timezone.datetime.combine(selected_date, timezone.datetime.min.time()))
            log.save()
            # Add TimelineEvent
            TimelineEvent.objects.create(
                user=request.user,
                timestamp=log.timestamp,
                title=f"Logged meal: {log.meal_type.title()}",
                event_type="meal_log",
                summary=f"{log.description} ({log.calories or 0} kcal)",
            )
            messages.success(request, "Meal logged and added to timeline.")
            return redirect(f"{request.path}?date={selected_date}")
    else:
        form = FoodLogForm()

    # Get all logs for the selected date
    logs = FoodLog.objects.filter(user=request.user, timestamp__date=selected_date).order_by('timestamp')
    total_calories = sum([log.calories or 0 for log in logs])

    return render(request, 'nutrition/food_log_summary.html', {
        'form': form,
        'logs': logs,
        'selected_date': selected_date,
        'total_calories': total_calories,
    })