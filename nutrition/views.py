from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FoodLog
from .forms import FoodLogForm

@login_required
def food_log_view(request):
    if request.method == 'POST':
        form = FoodLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('nutrition:food_log')
    else:
        form = FoodLogForm()
    logs = FoodLog.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'nutrition/food_log.html', {'form': form, 'logs': logs})