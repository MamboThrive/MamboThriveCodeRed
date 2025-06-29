# urls.py for the health_data app
# This file defines URL patterns for the health_data application.
# Add new routes here to connect views to URLs within the health_data app.

from django.urls import path
from . import views

app_name = 'health_data'  # Namespacing for the health_data app

urlpatterns = [
    path('results/', views.test_result_view, name='health_test_results'),
    path('results/add/', views.health_test_create, name='health_test_create'),
    path('results/edit/<int:pk>/', views.edit_test_result, name='edit_test_result'),
    path('results/delete/<int:pk>/', views.delete_test_result, name='delete_test_result'),
    path('results/delete_by_date/', views.delete_test_results_by_date, name='delete_test_results_by_date'),
    path('results/bulk_rename/', views.bulk_rename_test_name, name='bulk_rename_test_name'),
    path('uploads/', views.lab_upload_view, name='lab_report_uploads'),
    path("upload/json/", views.health_test_json_upload, name="health_test_json_upload"),
]
