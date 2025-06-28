from django import forms
from .models import FoodLog

class FoodLogForm(forms.ModelForm):
    class Meta:
        model = FoodLog
        fields = ['meal_type', 'description', 'calories', 'protein', 'fat', 'carbohydrates']
