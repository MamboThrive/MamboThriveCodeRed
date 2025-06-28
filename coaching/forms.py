from django import forms
from .models import HealthGoal, CoachMessage

class HealthGoalForm(forms.ModelForm):
    class Meta:
        model = HealthGoal
        fields = ['name', 'description', 'start_date', 'target_date', 'completed']

class CoachMessageForm(forms.ModelForm):
    class Meta:
        model = CoachMessage
        fields = ['message', 'source']
