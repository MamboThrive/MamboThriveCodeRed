from django.contrib import admin
from .models import UserKPI

# Register UserKPI model
@admin.register(UserKPI)
class UserKPIAdmin(admin.ModelAdmin):
    list_display = ('user', 'kpi_name', 'value', 'unit', 'date')
    search_fields = ('user__username', 'kpi_name')
    list_filter = ('kpi_name', 'date')
