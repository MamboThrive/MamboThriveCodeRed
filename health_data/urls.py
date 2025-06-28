# urls.py for the health_data app
# This file defines URL patterns for the health_data application.
# Add new routes here to connect views to URLs within the health_data app.

from django.urls import path
from . import views

app_name = 'health_data'  # Namespacing for the health_data app

urlpatterns = [
    path('results/', views.health_test_results, name='health_test_results'),
    path('uploads/', views.lab_report_uploads, name='lab_report_uploads'),
]
