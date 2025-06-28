from django.contrib import admin
from .models import HealthGoal, CoachMessage

# Register HealthGoal and CoachMessage models
@admin.register(HealthGoal)
class HealthGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'start_date', 'target_date', 'completed')
    search_fields = ('user__username', 'name')
    list_filter = ('completed', 'start_date', 'target_date')

@admin.register(CoachMessage)
class CoachMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'source')
    search_fields = ('user__username', 'message', 'source')
    list_filter = ('source', 'created_at')
