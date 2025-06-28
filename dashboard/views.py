from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserKPI
from datetime import date

@login_required
def dashboard_view(request):
    today = date.today()
    kpis = UserKPI.objects.filter(user=request.user, date=today)
    return render(request, 'dashboard/dashboard.html', {'kpis': kpis})