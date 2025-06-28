from django.db import models
from django.conf import settings

class HealthTestResult(models.Model):
    """
    Stores a single health test result (e.g., LDL, HbA1c, Blood Pressure).
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_date = models.DateField()
    test_name = models.CharField(max_length=255)  # e.g., "LDL Cholesterol"
    result_value = models.FloatField()
    unit = models.CharField(max_length=50)
    reference_range_min = models.FloatField(null=True, blank=True)
    reference_range_max = models.FloatField(null=True, blank=True)
    flagged = models.BooleanField(default=False)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-test_date']

    def __str__(self):
        return f"{self.user.username} - {self.test_name} on {self.test_date}"

class LabReportUpload(models.Model):
    """
    Stores raw uploaded files (PDFs, JSONs) for future parsing and extraction.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='lab_reports/')
    source = models.CharField(max_length=100, blank=True, help_text="Hospital or clinic name")
    parsed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} upload on {self.uploaded_at}"
