# core/models/snippets.py

from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel

@register_snippet
class HealthRange(models.Model):
    METRIC_CHOICES = [
        ('LDL', 'LDL Cholesterol'),
        ('HDL', 'HDL Cholesterol'),
        ('TG', 'Triglycerides'),
        ('GLU', 'Fasting Glucose'),
        # Extend as needed
    ]

    metric = models.CharField(max_length=20, choices=METRIC_CHOICES)
    age_min = models.PositiveIntegerField()
    age_max = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Male'), ('F', 'Female'), ('A', 'Any')]
    )
    min_value = models.FloatField()
    max_value = models.FloatField()
    unit = models.CharField(max_length=20)

    panels = [
        FieldPanel("metric"),
        FieldPanel("age_min"),
        FieldPanel("age_max"),
        FieldPanel("gender"),
        FieldPanel("min_value"),
        FieldPanel("max_value"),
        FieldPanel("unit"),
    ]

    def __str__(self):
        return f"{self.get_metric_display()} ({self.gender} {self.age_min}-{self.age_max})"


@register_snippet
class ConditionTag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.name


@register_snippet
class ReminderRule(models.Model):
    title = models.CharField(max_length=100)
    trigger_metric = models.CharField(max_length=20, choices=HealthRange.METRIC_CHOICES)
    condition = models.CharField(max_length=100, help_text="e.g., value > 130")
    message = models.TextField(help_text="What should the reminder say?")

    def __str__(self):
        return f"{self.title}: if {self.trigger_metric} → {self.condition}"

    panels = [
        FieldPanel("title"),
        FieldPanel("trigger_metric"),
        FieldPanel("condition"),
        FieldPanel("message"),
    ]
