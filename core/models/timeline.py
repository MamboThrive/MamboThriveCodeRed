from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class TimelineEvent(models.Model):
    # Owner of the event
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timeline_events')

    # When the event occurred (not necessarily created)
    timestamp = models.DateTimeField()

    # Label for UI display
    title = models.CharField(max_length=255)

    # Event category (used for filtering and icon selection)
    EVENT_TYPE_CHOICES = [
        ('test_result', 'Test Result'),
        ('meal_log', 'Meal'),
        ('sleep_log', 'Sleep'),
        ('exercise', 'Exercise'),
        ('symptom', 'Symptom'),
        ('medication', 'Medication'),
        ('note', 'Note'),
        ('goal', 'Goal'),
        ('visit', 'Doctor Visit'),
        ('other', 'Other'),
    ]
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, default='other')

    SEVERITY_CHOICES = [
        ('normal', 'Normal'),
        ('mild', 'Mild Concern'),
        ('moderate', 'Moderate Concern'),
        ('high', 'High Risk'),
    ]

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        blank=True,
        null=True,
        default='normal',
        help_text="Optional severity label for this event"
    )

    icon_class = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Optional Tailwind or Lucide icon class (e.g., 'flask', 'apple', 'pill')"
    )

    # Optional description
    summary = models.TextField(blank=True, null=True)

    # Generic relation to any linked model
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    color_tag = models.CharField(max_length=20, blank=True, null=True, help_text="Color for event type")

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.get_event_type_display()}] {self.title} ({self.timestamp.strftime('%Y-%m-%d')})"
    
    def save(self, *args, **kwargs):
        if not self.color_tag:
            self.color_tag = {
                'test_result': 'blue',
                'meal_log': 'green',
                'symptom': 'yellow',
                'medication': 'gray',
                'sleep_log': 'blue',
                'exercise': 'green',
            }.get(self.event_type, 'gray')
        super().save(*args, **kwargs)

