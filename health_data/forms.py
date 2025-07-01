from django import forms
from .models import HealthTestResult, LabReportUpload

class HealthTestResultForm(forms.ModelForm):
    class Meta:
        model = HealthTestResult
        fields = [
            'test_date', 'test_name', 'result_value',
            'unit', 'reference_range_min', 'reference_range_max',
            'flagged', 'tags', 'note',
        ]
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 2}),
        }

class LabReportUploadForm(forms.ModelForm):
    class Meta:
        model = LabReportUpload
        fields = ['file', 'source']

# health_data/forms.py

class HealthTestResultUploadForm(forms.Form):
    json_file = forms.FileField()

class PDFExtractForm(forms.Form):
    pdf_file = forms.FileField(label="Upload Health Exam PDF")
    source = forms.CharField(label="Source (Hospital/Clinic)", max_length=100, required=False)

