from django import forms
from .models import HealthTestResult, LabReportUpload

class HealthTestResultForm(forms.ModelForm):
    class Meta:
        model = HealthTestResult
        fields = ['test_date', 'test_name', 'result_value', 'unit', 'reference_range_min', 'reference_range_max', 'flagged', 'note']

class LabReportUploadForm(forms.ModelForm):
    class Meta:
        model = LabReportUpload
        fields = ['file', 'source']
