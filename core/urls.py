# urls.py for the core app
# This file defines URL patterns for the core application.
# Add new routes here to connect views to URLs within the core app.

from django.urls import path
from . import views

app_name = 'core'  # Namespacing for the core app

urlpatterns = [
    path('timeline/', views.timeline_view, name='timeline'),
    path('timeline/events/', views.timeline_event_list, name='timeline_events'),
]
