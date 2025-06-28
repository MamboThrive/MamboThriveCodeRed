from django import forms
from .models import UserKPI

class UserKPIForm(forms.ModelForm):
    class Meta:
        model = UserKPI
        fields = ['date', 'kpi_name', 'value', 'unit']
