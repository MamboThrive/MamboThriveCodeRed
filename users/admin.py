from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register the custom user model with the Django admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Add custom fields to the admin if needed
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    list_display = UserAdmin.list_display + ('role',)
    list_filter = ('role', 'is_staff')
