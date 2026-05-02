from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('passport/', views.passport, name='passport'),
    path('vendor/', views.host_workspace, name='vendor'),
    path('vendor/experiences/new/', views.vendor_experience_create, name='vendor_experience_create'),
    path('host/', views.host_workspace, name='host'),
    path('host/experiences/new/', views.vendor_experience_create, name='host_experience_create'),
    path('admin-workspace/', views.admin_workspace, name='admin_workspace'),
]
