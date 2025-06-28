# urls.py for the dashboard app
# This file defines URL patterns for the dashboard application.
# Add new routes here to connect views to URLs within the dashboard app.

from django.urls import path
from . import views

app_name = 'dashboard'  # Namespacing for the dashboard app

urlpatterns = [
    # Route for the dashboard_view
    path('', views.dashboard_view, name='dashboard'),
]
