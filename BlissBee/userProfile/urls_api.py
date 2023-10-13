# urls.py
from django.urls import path
from . import views_api as views

urlpatterns = [
    path('api/register/', views.register, name='api_register'),
    path('api/login/', views.login_view, name='api_login'),
    path('api/dashboard/', views.dashboard, name='api_dashboard'),
    path('api/user_logout/', views.user_logout, name='user_logout'),
    # Other URL patterns for your application
]