# apps.py - AppConfig for the health_data Django app
# This file defines the configuration for the health_data application.
# AppConfig allows you to specify application-specific settings and metadata.

from django.apps import AppConfig

class HealthDataConfig(AppConfig):
    # Specifies the default type for auto-generated primary keys
    default_auto_field = 'django.db.models.BigAutoField'
    # The full Python path to the application (should match the app directory name)
    name = 'health_data'
    # Human-readable name for the app in the Django admin and elsewhere
    verbose_name = "Health Exam Data"
    # Short label for the app (must be a valid Python identifier and unique across all apps)
    label = 'health_data'