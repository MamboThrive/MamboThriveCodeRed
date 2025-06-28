# apps.py - AppConfig for the core Django app
# This file defines the configuration for the core application.
# AppConfig allows you to specify application-specific settings and metadata.

from django.apps import AppConfig


class CoreConfig(AppConfig):
    # Specifies the default type for auto-generated primary keys
    default_auto_field = 'django.db.models.BigAutoField'
    # The full Python path to the application (should match the app directory name)
    name = 'core'
    # Human-readable name for the app in the Django admin and elsewhere
    verbose_name = "Core Utilities"
    # Short label for the app (should be unique across all apps in the project)
    label = 'core'
