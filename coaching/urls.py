# urls.py for the coaching app
# This file defines URL patterns for the coaching application.
# Add new routes here to connect views to URLs within the coaching app.

from django.urls import path
from . import views

app_name = 'coaching'  # Namespacing for the coaching app

urlpatterns = [
    # Route for the coaching app's index page
    path('', views.coaching_view, name='coaching_overview'),
]
