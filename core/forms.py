from django import forms
from .models import TimelineEvent

class TimelineEventForm(forms.ModelForm):
    class Meta:
        model = TimelineEvent
        fields = ['event_type', 'summary']
