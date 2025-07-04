from collections import defaultdict
from django.utils.dateformat import format as date_format
import json as pyjson
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HealthTestResult
from .forms import HealthTestResultForm
from django.contrib import messages
import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def test_result_view(request):
    # Filtering
    filters = Q(user=request.user)
    test_name = request.GET.get('test_name', '').strip()
    test_date = request.GET.get('test_date', '').strip()
    result_value = request.GET.get('result_value', '').strip()
    unit = request.GET.get('unit', '').strip()
    flagged = request.GET.get('flagged', '').strip()
    order_by = request.GET.get('sort', '-test_date')

    if test_name:
        filters &= Q(test_name__icontains=test_name)
    if test_date:
        filters &= Q(test_date=test_date)
    if result_value:
        try:
            filters &= Q(result_value=float(result_value))
        except ValueError:
            pass
    if unit:
        filters &= Q(unit__icontains=unit)
    if flagged == 'true':
        filters &= Q(flagged=True)
    elif flagged == 'false':
        filters &= Q(flagged=False)

    # Sorting
    allowed_sorts = ['test_name', '-test_name', 'test_date', '-test_date', 'result_value', '-result_value', 'unit', '-unit', 'flagged', '-flagged']
    if order_by not in allowed_sorts:
        order_by = '-test_date'

    results_qs = HealthTestResult.objects.filter(filters).order_by(order_by)

    # Pagination
    paginator = Paginator(results_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # --- Chart Data Preparation ---
    all_results = HealthTestResult.objects.filter(user=request.user)
    chart_metrics = sorted(set(all_results.values_list('test_name', flat=True)))
    chart_data = {}
    grouped = defaultdict(list)
    for r in all_results:
        grouped[r.test_name].append(r)
    for metric, items in grouped.items():
        # Sort by date
        items_sorted = sorted(items, key=lambda x: x.test_date)
        dates = [date_format(x.test_date, 'Y-m-d') for x in items_sorted]
        values = [x.result_value for x in items_sorted]
        # Use the most common unit, or the first
        unit = items_sorted[0].unit if items_sorted else ''
        # Reference range: use the most common, or the first non-null
        min_vals = [x.reference_range_min for x in items_sorted if x.reference_range_min is not None]
        max_vals = [x.reference_range_max for x in items_sorted if x.reference_range_max is not None]
        min_val = min_vals[0] if min_vals else None
        max_val = max_vals[0] if max_vals else None
        chart_data[metric] = {
            'dates': dates,
            'values': values,
            'min': min_val,
            'max': max_val,
            'unit': unit,
        }
    chart_data_json = pyjson.dumps(chart_data)
    # --- End Chart Data Preparation ---

    form = HealthTestResultForm()
    if request.method == 'POST':
        form = HealthTestResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.user = request.user
            result.save()
            form.save_m2m()
            messages.success(request, "Test result added.")
            return redirect('health_data:health_test_results')
    return render(request, 'health_data/health_test_results.html', {
        'form': form,
        'results': page_obj,
        'page_obj': page_obj,
        'request': request,
        'order_by': order_by,
        'chart_metrics': chart_metrics,
        'chart_data_json': chart_data_json,
    })

@login_required
@require_POST
def delete_test_result(request, pk):
    result = HealthTestResult.objects.filter(user=request.user, pk=pk).first()
    if result:
        result.delete()
        messages.success(request, "Test result deleted.")
    return redirect('health_data:health_test_results')

@login_required
@require_POST
def delete_test_results_by_date(request):
    date = request.POST.get('test_date')
    if date:
        deleted, _ = HealthTestResult.objects.filter(user=request.user, test_date=date).delete()
        messages.success(request, f"Deleted {deleted} test result(s) for {date}.")
    return redirect('health_data:health_test_results')

@login_required
def edit_test_result(request, pk):
    result = HealthTestResult.objects.filter(user=request.user, pk=pk).first()
    if not result:
        return redirect('health_data:health_test_results')
    if request.method == 'POST':
        form = HealthTestResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, "Test result updated.")
            return redirect('health_data:health_test_results')
    else:
        form = HealthTestResultForm(instance=result)
    return render(request, 'health_data/health_test_form.html', {'form': form, 'edit': True, 'result': result})

@login_required
def bulk_rename_test_name(request):
    if request.method == 'POST':
        old_name = request.POST.get('old_name')
        new_name = request.POST.get('new_name')
        if old_name and new_name:
            updated = HealthTestResult.objects.filter(user=request.user, test_name=old_name).update(test_name=new_name)
            messages.success(request, f"Renamed {updated} test(s) from '{old_name}' to '{new_name}'.")
            return redirect('health_data:health_test_results')
    return render(request, 'health_data/bulk_rename_test_name.html')

@login_required
def health_test_create(request):
    if request.method == 'POST':
        form = HealthTestResultForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.user = request.user
            test.save()
            form.save_m2m()

            # Timeline integration


            return redirect('health_data:health_test_results')
    else:
        form = HealthTestResultForm()
    return render(request, 'health_data/health_test_form.html', {'form': form})

@login_required
@require_POST
def health_test_json_upload(request):
    if request.method == 'POST':
        json_file = request.FILES.get('json_file')
        if not json_file:
            messages.error(request, 'No file uploaded.')
            return redirect('health_data:health_test_results')
        try:
            data = json.load(json_file)
            results = data.get('results', [])
            success_count = 0
            failure_count = 0
            for entry in results:
                try:
                    HealthTestResult.objects.create(
                        user=request.user,
                        test_date=entry['test_date'],
                        test_name=entry['test_name'],
                        result_value=entry['result_value'],
                        unit=entry.get('unit'),
                        reference_range_min=entry.get('reference_range_min'),
                        reference_range_max=entry.get('reference_range_max'),
                        flagged=entry.get('flagged', False),
                        note=entry.get('note', '')
                    )
                    success_count += 1
                except Exception as e:
                    failure_count += 1
            if success_count:
                messages.success(request, f"Successfully uploaded {success_count} result(s).")
            if failure_count:
                messages.warning(request, f"{failure_count} result(s) failed to import.")
        except Exception as e:
            messages.error(request, f"Error processing file: {e}")
    return redirect('health_data:health_test_results')

