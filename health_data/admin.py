from django.contrib import admin
from .models import HealthTestResult, LabReportUpload

# Register HealthTestResult and LabReportUpload models
@admin.register(HealthTestResult)
class HealthTestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_name', 'test_date', 'result_value', 'unit', 'flagged')
    search_fields = ('user__username', 'test_name')
    list_filter = ('test_name', 'flagged', 'test_date')

@admin.register(LabReportUpload)
class LabReportUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'uploaded_at', 'source', 'parsed')
    search_fields = ('user__username', 'source')
    list_filter = ('parsed', 'source')
