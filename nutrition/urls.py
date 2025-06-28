# urls.py for the nutrition app
# This file defines URL patterns for the nutrition application.
# Add new routes here to connect views to URLs within the nutrition app.

from django.urls import path
from . import views

app_name = 'nutrition'  # Namespacing for the nutrition app

urlpatterns = [
    # Route for viewing food logs
    path('logs/', views.food_log_view, name='food_log'),
]
