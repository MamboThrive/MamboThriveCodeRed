from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from health_data.models import HealthTestResult
from nutrition.models import FoodLog
from datetime import date
from django.db.models import Q, Max, Sum
import json

@login_required
def dashboard_view(request):
    user = request.user
    today = date.today()

    # Latest LDL, HDL, Glucose
    def get_latest_metric(test_name):
        return HealthTestResult.objects.filter(user=user, test_name__iexact=test_name).order_by('-test_date').first()
    ldl = get_latest_metric('LDL')
    hdl = get_latest_metric('HDL')
    glucose = get_latest_metric('Glucose')

    # Provide default metric object if None
    class DummyMetric:
        result_value = None
        unit = ''
        test_date = None
    if ldl is None:
        ldl = DummyMetric()
    if hdl is None:
        hdl = DummyMetric()
    if glucose is None:
        glucose = DummyMetric()

    # Out-of-range count
    out_of_range_count = HealthTestResult.objects.filter(user=user, flagged=True).count()

    # Today's total calories
    calories_today = FoodLog.objects.filter(user=user, timestamp__date=today).aggregate(total=Sum('calories'))['total'] or 0

    # For summary charts (last 7 values)
    def get_metric_trend(test_name):
        qs = HealthTestResult.objects.filter(user=user, test_name__iexact=test_name).order_by('-test_date')[:7]
        # Convert date objects to ISO strings for JSON serialization
        return [[d.isoformat(), v] for d, v in qs.values_list('test_date', 'result_value')][::-1]  # oldest first
    ldl_trend = get_metric_trend('LDL')
    hdl_trend = get_metric_trend('HDL')
    glucose_trend = get_metric_trend('Glucose')

    show_alert = out_of_range_count > 0

    # Serialize trends as JSON for safe JS injection
    ldl_trend_json = json.dumps(ldl_trend)
    hdl_trend_json = json.dumps(hdl_trend)
    glucose_trend_json = json.dumps(glucose_trend)

    return render(request, 'dashboard/dashboard.html', {
        'ldl': ldl,
        'hdl': hdl,
        'glucose': glucose,
        'calories_today': calories_today,
        'out_of_range_count': out_of_range_count,
        'show_alert': show_alert,
        'ldl_trend_json': ldl_trend_json,
        'hdl_trend_json': hdl_trend_json,
        'glucose_trend_json': glucose_trend_json,
    })