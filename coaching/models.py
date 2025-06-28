from django.db import models
from django.conf import settings

class HealthGoal(models.Model):
    """
    Stores a user-defined health goal (e.g., weight loss, cholesterol reduction).
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    target_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Goal: {self.name}"

class CoachMessage(models.Model):
    """
    AI or human-generated coaching messages for a user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    source = models.CharField(max_length=50, choices=[('ai', 'AI'), ('human', 'Human')], default='ai')

    def __str__(self):
        return f"{self.source.title()} Coach Message for {self.user.username} @ {self.created_at}"