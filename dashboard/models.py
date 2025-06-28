from django.db import models
from django.conf import settings

class UserKPI(models.Model):
    """
    Stores daily/weekly/monthly KPIs (e.g., steps, average sleep, LDL levels).
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    kpi_name = models.CharField(max_length=100)  # E.g., "LDL", "Steps", "SleepHours"
    value = models.FloatField()
    unit = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ('user', 'date', 'kpi_name')

    def __str__(self):
        return f"{self.user.username} - {self.kpi_name} = {self.value} on {self.date}"