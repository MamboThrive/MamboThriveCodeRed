from django.contrib import admin
from .models import FoodLog

# Register FoodLog model
@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_type', 'timestamp', 'calories')
    search_fields = ('user__username', 'meal_type', 'description')
    list_filter = ('meal_type', 'timestamp')
