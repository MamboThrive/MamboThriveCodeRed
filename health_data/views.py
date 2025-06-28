from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HealthTestResult, LabReportUpload
from .forms import HealthTestResultForm, LabReportUploadForm

@login_required
def test_result_view(request):
    if request.method == 'POST':
        form = HealthTestResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.user = request.user
            result.save()
            return redirect('health_data:test_result')
    else:
        form = HealthTestResultForm()
    results = HealthTestResult.objects.filter(user=request.user)
    return render(request, 'health_data/test_results.html', {'form': form, 'results': results})

@login_required
def lab_upload_view(request):
    if request.method == 'POST':
        form = LabReportUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            return redirect('health_data:lab_upload')
    else:
        form = LabReportUploadForm()
    uploads = LabReportUpload.objects.filter(user=request.user)
    return render(request, 'health_data/lab_upload.html', {'form': form, 'uploads': uploads})