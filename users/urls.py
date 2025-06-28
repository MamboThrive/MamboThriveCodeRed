# urls.py for the users app
# This file defines URL patterns for the users application.
# Add new routes here to connect views to URLs within the users app.

from django.urls import include, path
from . import views

app_name = 'users'  # Namespacing for the users app

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_view, name='activate'),
    path('password_reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/', include('allauth.urls')),
]
