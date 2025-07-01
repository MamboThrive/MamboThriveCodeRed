from django.db import models
from django.conf import settings
from modelcluster.fields import ParentalManyToManyField

class HealthTestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_date = models.DateField()
    test_name = models.CharField(max_length=255)
    result_value = models.FloatField()
    unit = models.CharField(max_length=50, null=True, blank=True)
    reference_range_min = models.FloatField(null=True, blank=True)
    reference_range_max = models.FloatField(null=True, blank=True)
    flagged = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)

    tags = ParentalManyToManyField("core.ConditionTag", blank=True)

    # Phase 2+ Fields
    ai_interpretation = models.TextField(blank=True)
    interpretation_confidence = models.FloatField(null=True, blank=True)
    is_trending_up = models.BooleanField(null=True, blank=True)
    is_trending_down = models.BooleanField(null=True, blank=True)
    standardized_code = models.CharField(max_length=50, blank=True)

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
